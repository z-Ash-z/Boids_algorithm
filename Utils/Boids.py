from __future__ import annotations
import numpy as np

class Boids:
    
    def __init__(self, num_boids: int, width: int, height: int) -> None:
        """
        The Boids class that manages all boids using NumPy for optimized performance.
        
        Args:
            num_boids: The number of boids to simulate.
            width: The width of the stage in pixels.
            height: The height of the stage in pixels.
        """
        self.num_boids = num_boids
        self.WIDTH = width
        self.HEIGHT = height
        
        # Initialize positions, velocities, and accelerations
        self.positions = np.random.rand(num_boids, 2) * np.array([width, height])
        self.velocities = np.random.uniform(-1, 1, (num_boids, 2))
        self.accelerations = np.zeros((num_boids, 2))
        
        # Constants
        self.ALIGNMENT_RADIUS = 100
        self.COHESION_RADIUS = 200
        self.SEPERATION_RADIUS = 20
        
        self.MAX_ALIGNMENT_FORCE = 0.01
        self.MAX_COHESION_FORCE = 0.015
        self.MAX_SEPERATION_FORCE = 0.1
        self.MAX_SPEED = 1.0

    def flock(self) -> None:
        """
        Uses alignment, cohesion and separation properties to update accelerations for all boids.
        """
        # Reset accelerations
        self.accelerations = np.zeros_like(self.positions)
        
        # Calculate distance matrix (N, N)
        # Using broadcasting: (N, 1, 2) - (1, N, 2) -> (N, N, 2)
        pos = self.positions
        diff = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]
        dist = np.linalg.norm(diff, axis=2)
        
        # Avoid self-interaction by setting diagonal to infinity
        np.fill_diagonal(dist, np.inf)
        
        # --- Alignment ---
        # Average velocity of neighbors within radius
        mask_align = dist < self.ALIGNMENT_RADIUS
        counts_align = mask_align.sum(axis=1, keepdims=True)
        
        # Sum velocities of neighbors: (N, N) @ (N, 2) -> (N, 2)
        align_sum = mask_align @ self.velocities
        
        # Calculate average and apply limit
        alignment = np.zeros_like(self.velocities)
        np.divide(align_sum, counts_align, out=alignment, where=counts_align > 0)
        alignment = self._limit_vector(alignment, self.MAX_ALIGNMENT_FORCE)
        
        # --- Cohesion ---
        # Steer towards average position of neighbors
        mask_coh = dist < self.COHESION_RADIUS
        counts_coh = mask_coh.sum(axis=1, keepdims=True)
        
        coh_sum = mask_coh @ self.positions
        
        cohesion = np.zeros_like(self.positions)
        np.divide(coh_sum, counts_coh, out=cohesion, where=counts_coh > 0)
        
        # Steer towards target (average pos) - current pos
        # Only apply if we have neighbors (where counts > 0)
        has_neighbors_coh = counts_coh.flatten() > 0
        cohesion[has_neighbors_coh] -= self.positions[has_neighbors_coh]
        
        cohesion = self._limit_vector(cohesion, self.MAX_COHESION_FORCE)
        
        # --- Separation ---
        # Steer away from neighbors: sum((self_pos - other_pos) / dist)
        mask_sep = dist < self.SEPERATION_RADIUS
        counts_sep = mask_sep.sum(axis=1, keepdims=True)
        
        # diff is (self - other). We want to normalize by distance.
        # Avoid division by zero (inf in dist)
        with np.errstate(divide='ignore', invalid='ignore'):
            weighted_diff = diff / dist[:, :, np.newaxis]
        
        # Sum weighted diffs for neighbors
        # weighted_diff: (N, N, 2), mask_sep: (N, N) -> expand to (N, N, 1)
        sep_sum = (weighted_diff * mask_sep[:, :, np.newaxis]).sum(axis=1)
        
        separation = np.zeros_like(self.positions)
        np.divide(sep_sum, counts_sep, out=separation, where=counts_sep > 0)
        
        separation = self._limit_vector(separation, self.MAX_SEPERATION_FORCE)
        
        # --- Combine Forces ---
        # Original logic: acceleration = separation + cohesion + alignment
        # Note: The original code accumulated them:
        # cohesion.add(alignment)
        # seperation.add(cohesion)
        # self.acceleration = seperation
        # So it is indeed the sum.
        
        self.accelerations = alignment + cohesion + separation

    def update(self) -> None:
        """
        Update positions based on velocity and acceleration.
        """
        self.velocities += self.accelerations
        self.velocities = self._limit_vector(self.velocities, self.MAX_SPEED)
        self.positions += self.velocities
        self._edges()

    def _edges(self) -> None:
        """
        Wrap positions around the stage edges.
        """
        self.positions[:, 0] = np.where(self.positions[:, 0] >= self.WIDTH, 0, self.positions[:, 0])
        self.positions[:, 0] = np.where(self.positions[:, 0] <= 0, self.WIDTH, self.positions[:, 0])
        self.positions[:, 1] = np.where(self.positions[:, 1] >= self.HEIGHT, 0, self.positions[:, 1])
        self.positions[:, 1] = np.where(self.positions[:, 1] <= 0, self.HEIGHT, self.positions[:, 1])

    def _limit_vector(self, vectors: np.ndarray, limit: float) -> np.ndarray:
        """
        Limit the components of vectors to [-limit, limit].
        Matches the original Vector.limit behavior (component-wise clamping).
        """
        return np.clip(vectors, -limit, limit)

    def get_positions(self) -> np.ndarray:
        return self.positions