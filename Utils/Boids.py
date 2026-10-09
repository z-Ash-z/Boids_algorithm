from __future__ import annotations
import numpy as np

# Try importing CuPy for CUDA GPU acceleration
try:
    import cupy as cp
    CUDA_AVAILABLE = cp.cuda.is_available() and cp.cuda.runtime.getDeviceCount() > 0
except Exception:
    CUDA_AVAILABLE = False
    cp = None


class Boids:
    
    def __init__(self, num_boids: int, width: int, height: int, device: str = 'auto') -> None:
        """
        The Boids class that manages all boids with Craig Reynolds steering aerodynamics,
        toroidal wrap-aware perception, and automatic CUDA GPU / optimized CPU execution.
        
        Args:
            num_boids: The number of boids to simulate.
            width: The width of the stage in pixels.
            height: The height of the stage in pixels.
            device: 'cuda', 'cpu', or 'auto' (defaults to 'cuda' if available).
        """
        self.num_boids = num_boids
        self.WIDTH = width
        self.HEIGHT = height
        
        # Determine execution device
        if device == 'auto':
            self.use_cuda = CUDA_AVAILABLE
        elif device == 'cuda':
            if not CUDA_AVAILABLE:
                print("Warning: CUDA requested but not available. Falling back to CPU.")
            self.use_cuda = CUDA_AVAILABLE
        else:
            self.use_cuda = False

        self.xp = cp if self.use_cuda else np
        
        # Flocking perception & force parameters (Reynolds Steering)
        self.ALIGNMENT_RADIUS = 100.0
        self.COHESION_RADIUS = 180.0
        self.SEPERATION_RADIUS = 35.0
        
        self.MAX_ALIGNMENT_FORCE = 0.05
        self.MAX_COHESION_FORCE = 0.04
        self.MAX_SEPERATION_FORCE = 0.12
        
        # Aerodynamic speed limits
        self.MIN_SPEED = 1.5
        self.MAX_SPEED = 4.0
        
        # Field of View (FOV): 270 degrees (leaving a 90-degree blind spot behind the tail)
        self.FOV_DEGREES = 270.0
        self.cos_half_fov = float(np.cos(np.radians(self.FOV_DEGREES / 2.0)))

        # Initialize positions and velocities
        init_pos = np.random.rand(num_boids, 2).astype(np.float32) * np.array([width, height], dtype=np.float32)
        init_vel = np.random.uniform(-1.0, 1.0, (num_boids, 2)).astype(np.float32)
        # Normalize to cruising speed
        speeds = np.linalg.norm(init_vel, axis=1, keepdims=True)
        init_vel = (init_vel / np.maximum(speeds, 1e-6)) * 2.5
        
        if self.use_cuda:
            self.positions = cp.asarray(init_pos)
            self.velocities = cp.asarray(init_vel)
            self.accelerations = cp.zeros((num_boids, 2), dtype=cp.float32)
            self._host_positions = init_pos
            self._host_velocities = init_vel
        else:
            self.positions = init_pos
            self.velocities = init_vel
            self.accelerations = np.zeros((num_boids, 2), dtype=np.float32)
            self._host_positions = self.positions
            self._host_velocities = self.velocities

    @property
    def device_name(self) -> str:
        if self.use_cuda:
            dev_name = cp.cuda.runtime.getDeviceProperties(0)['name'].decode()
            return f"CUDA ({dev_name})"
        return "CPU (NumPy)"

    @staticmethod
    def get_default_device_name() -> str:
        if CUDA_AVAILABLE:
            dev_name = cp.cuda.runtime.getDeviceProperties(0)['name'].decode()
            return f"CUDA ({dev_name})"
        return "CPU (NumPy)"

    @staticmethod
    def _limit_magnitude(xp, vectors, max_mag: float, min_mag: float = 0.0):
        """
        Limits vector lengths radially without distorting their heading angles.
        """
        norms = xp.linalg.norm(vectors, axis=-1, keepdims=True)
        safe_norms = xp.maximum(norms, 1e-6)
        unit = vectors / safe_norms
        clamped_mag = xp.clip(norms, min_mag, max_mag)
        return unit * clamped_mag

    def flock(self) -> None:
        """
        Calculates Craig Reynolds steering forces across all boids using
        toroidal wrap-aware relative coordinates and perception cones.
        """
        xp = self.xp
        pos = self.positions
        vel = self.velocities
        
        # 1. Toroidal relative vectors (Minimum Image Convention)
        # diff points from neighbor j to self i: pos[i] - pos[j]
        stage_dims = xp.array([self.WIDTH, self.HEIGHT], dtype=xp.float32)
        diff = pos[:, None, :] - pos[None, :, :]
        diff = diff - stage_dims * xp.round(diff / stage_dims)
        dist = xp.linalg.norm(diff, axis=2)
        xp.fill_diagonal(dist, xp.inf)
        
        # 2. Field of View (Perception Cone)
        # Boid headings: (N, 2)
        speeds = xp.linalg.norm(vel, axis=1, keepdims=True)
        headings = vel / xp.maximum(speeds, 1e-6)
        # Vector from self to neighbor is -diff
        dir_to_nbr = -diff / xp.maximum(dist[:, :, None], 1e-6)
        cos_angles = (headings[:, None, :] * dir_to_nbr).sum(axis=2)
        in_fov = cos_angles >= self.cos_half_fov
        
        # --- Alignment (Reynolds Steering: steer toward average neighbor heading) ---
        mask_align = (dist < self.ALIGNMENT_RADIUS) & in_fov
        counts_align = mask_align.sum(axis=1, keepdims=True)
        sum_align_vel = mask_align.astype(xp.float32) @ vel
        avg_spd = xp.linalg.norm(sum_align_vel, axis=1, keepdims=True)
        desired_align = (sum_align_vel / xp.maximum(avg_spd, 1e-6)) * self.MAX_SPEED
        steer_align = xp.where(counts_align > 0, desired_align - vel, 0.0)
        steer_align = self._limit_magnitude(xp, steer_align, self.MAX_ALIGNMENT_FORCE)
        
        # --- Cohesion (Reynolds Steering: steer toward center of mass of neighbors) ---
        mask_coh = (dist < self.COHESION_RADIUS) & in_fov
        counts_coh = mask_coh.sum(axis=1, keepdims=True)
        # Relative center of mass is sum of (-diff) for neighbors
        sum_rel_pos = (-diff * mask_coh[:, :, None]).sum(axis=1)
        center_dist = xp.linalg.norm(sum_rel_pos, axis=1, keepdims=True)
        desired_coh = (sum_rel_pos / xp.maximum(center_dist, 1e-6)) * self.MAX_SPEED
        steer_coh = xp.where(counts_coh > 0, desired_coh - vel, 0.0)
        steer_coh = self._limit_magnitude(xp, steer_coh, self.MAX_COHESION_FORCE)
        
        # --- Separation (Reynolds Steering: smooth inverse-distance repulsion) ---
        # Separation checks 360 degrees to prevent rear/blind-spot collisions
        mask_sep = (dist < self.SEPERATION_RADIUS) & (dist > 1e-4)
        counts_sep = mask_sep.sum(axis=1, keepdims=True)
        # Weight force smoothly by inverse distance: 1 / max(dist, 0.01)
        inv_dist_weight = xp.where(mask_sep, 1.0 / xp.maximum(dist, 1e-2), 0.0)
        repel_force = (diff * inv_dist_weight[:, :, None]).sum(axis=1)
        repel_mag = xp.linalg.norm(repel_force, axis=1, keepdims=True)
        desired_sep = (repel_force / xp.maximum(repel_mag, 1e-6)) * self.MAX_SPEED
        steer_sep = xp.where(counts_sep > 0, desired_sep - vel, 0.0)
        steer_sep = self._limit_magnitude(xp, steer_sep, self.MAX_SEPERATION_FORCE)
        
        self.accelerations = steer_align + steer_coh + steer_sep

    def update(self) -> None:
        """
        Updates velocities with steering accelerations, clamps to [min_speed, max_speed],
        advances positions, and wraps cleanly across stage edges.
        """
        self.velocities += self.accelerations
        # Radial magnitude clamp with cruising speed
        self.velocities = self._limit_magnitude(self.xp, self.velocities, self.MAX_SPEED, self.MIN_SPEED)
        self.positions += self.velocities
        self._edges()
        
        # Cache host copies for Pygame rendering
        if self.use_cuda:
            self._host_positions = self.positions.get()
            self._host_velocities = self.velocities.get()
        else:
            self._host_positions = self.positions
            self._host_velocities = self.velocities

    def _edges(self) -> None:
        """
        Clean toroidal screen wrapping using modulo.
        """
        self.positions[:, 0] = self.positions[:, 0] % self.WIDTH
        self.positions[:, 1] = self.positions[:, 1] % self.HEIGHT

    def get_positions(self) -> np.ndarray:
        """Returns positions as a NumPy array on the host CPU for rendering."""
        return self._host_positions

    def get_velocities(self) -> np.ndarray:
        """Returns velocities as a NumPy array on the host CPU for rendering."""
        return self._host_velocities