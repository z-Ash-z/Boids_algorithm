from __future__ import annotations
    

class Vector():

    __vector_3D : bool
    
    def __init__(self, *args) -> None:
        """
        The vector class to store and deal with vector. This class can store both 2D and 3D vectors.

        Raises:
            IndexError: IF invalid number of inputs are used.
            TypeError: If the inputs are not float or int.
        """
        
        if len(args) == 0:
            self.x = 0
            self.y = 0
            self.z = 0
            self.__vector_3D = False
        else:
            if len(args) > 3 or len(args) < 2:
                raise IndexError("Accepts 2 args for 2D Vector and 3 args for 3D Vector.")

            for arg in args:
                if type(arg) is not float and type(arg) is not int:
                    raise TypeError("Only integers or float are allowed.")
                
            if len(args) == 3:
                self.__vector_3D = True
                self.x = args[0]
                self.y = args[1]
                self.z = args[2]
            else:
                self.__vector_3D = False
                self.x = args[0]
                self.y = args[1]

    def add(self, other) -> None:
        """
        The addtion function. Takes in another vector or a number and add its to the current vector.

        Args:
            other: An int, float or another vector.
        """
        if isinstance(other, Vector):
            if self.__vector_3D:
                self.x = (self.x + other.x)
                self.y = (self.y + other.y)
                self.z = (self.z + other.z)
            else:
                self.x = (self.x + other.x)
                self.y = (self.y + other.y)
        else:
            if self.__vector_3D:
                self.x = (self.x + other)
                self.y = (self.y + other)
                self.z = (self.z + other)
            else:
                self.x = (self.x + other)
                self.y = (self.y + other)

    def sub(self, other) -> None:
        """
        The subtraction function. Takes in another vector or a number and subtract from it from the current vector.

        Args:
            other: An int, float or another vector.
        """
        if isinstance(other, Vector):
            if self.__vector_3D:
                self.x = (self.x - other.x)
                self.y = (self.y - other.y)
                self.z = (self.z - other.z)
            else:
                self.x = (self.x - other.x)
                self.y = (self.y - other.y)
        else:
            if self.__vector_3D:
                self.x = (self.x - other)
                self.y = (self.y - other)
                self.z = (self.z - other)
            else:
                self.x = (self.x - other)
                self.y = (self.y - other)

    def multiply(self, other) -> None:
        """
        The multiplicaiton function. Takes in another vector or a number and multiplies it to the current vector.

        Args:
            other: An int, float or another vector.
        """
        if isinstance(other, Vector):
            if self.__vector_3D:
                self.x = (self.x * other.x)
                self.y = (self.y * other.y)
                self.z = (self.z * other.z)
            else:
                self.x = (self.x * other.x)
                self.y = (self.y * other.y)
        else:
            if self.__vector_3D:
                self.x = (self.x * other)
                self.y = (self.y * other)
                self.z = (self.z * other)
            else:
                self.x = (self.x * other)
                self.y = (self.y * other)

    def divide(self, other) -> None:
        """
        The division function. Takes in another vector or a number and divides the current vector.

        Args:
            other: An int, float or another vector.
        """
        if isinstance(other, Vector):
            if self.__vector_3D:
                self.x = (self.x / other.x)
                self.y = (self.y / other.y)
                self.z = (self.z / other.z)
            else:
                self.x = (self.x / other.x)
                self.y = (self.y / other.y)
        else:
            if self.__vector_3D:
                self.x = (self.x / other)
                self.y = (self.y / other)
                self.z = (self.z / other)
            else:
                self.x = (self.x / other)
                self.y = (self.y / other)

    def limit(self, limit):
        """
        A method that can limit the magnitude of the current vector to : (-limit < vector < limit)

        Args:
            limit: An integer or float to bound the vector.
        """
        limit = abs(limit)
        if self.__vector_3D:
            self.x = min(max(self.x, -limit), limit)
            self.y = min(max(self.y, -limit), limit)
            self.z = min(max(self.z, -limit), limit)
        else:
            self.x = min(max(self.x, -limit), limit)
            self.y = min(max(self.y, -limit), limit)

    def is3D(self) -> bool:
        """
        Function to return if the vector is 3D.

        Returns:
            True, if the vector is 3D.
        """
        return self.__vector_3D

    def __add__(self, other) -> Vector:
        """
        Operation overloading for Vector + other.

        Args:
            other: The other variable (int/float/vector).

        Returns:
            A vector with the variables added accordingly.
        """
        if isinstance(other, Vector):
            if self.__vector_3D:
                return Vector((self.x + other.x), (self.y + other.y), (self.z + other.z))
            return Vector((self.x + other.x), (self.y + other.y))
        if self.__vector_3D:
            return Vector((self.x + other), (self.y + other), (self.z + other))
        return Vector((self.x + other), (self.y + other))
        
    def __radd__(self, other) -> Vector:
        """
        Operation overloading for other + Vector.

        Args:
            other: The other variable (int/float/vector).

        Returns:
            A vector with the variables added accordingly.
        """
        return self.__add__(other)
    
    def __sub__(self, other) -> Vector:
        """
        Operation overloading for Vector - other.

        Args:
            other: The other variable (int/float/vector).

        Returns:
            A vector with the variables subtracted accordingly.
        """
        if isinstance(other, Vector):
            if self.__vector_3D:
                return Vector((self.x - other.x), (self.y - other.y), (self.z - other.z))
            return Vector((self.x - other.x), (self.y - other.y))
        if self.__vector_3D:
            return Vector((self.x - other), (self.y - other), (self.z - other))
        return Vector((self.x - other), (self.y - other))
        
    def __rsub__(self, other) -> Vector:
        """
        Operation overloading for other - Vector.

        Args:
            other: The other variable (int/float/vector).

        Returns:
            A vector with the variables subtracted accordingly.
        """

        if isinstance(other, Vector):
            if self.__vector_3D:
                return Vector((other.x - self.x), (other.y - self.y), (other.z - self.z))
            return Vector((other.x - self.x), (other.y - self.y))
        if self.__vector_3D:
            return Vector((other - self.x), (other - self.y), (other - self.z))
        return Vector((other - self.x), (other - self.y))
    
    def __mul__(self, other) -> Vector:
        """
        Operation overloading for Vector * other.

        Args:
            other: The other variable (int/float/vector).

        Returns:
            A vector with the variables multiplied accordingly.
        """
        if isinstance(other, Vector):
            if self.__vector_3D:
                return Vector((self.x * other.x), (self.y * other.y), (self.z * other.z))
            return Vector((self.x * other.x), (self.y * other.y))
        if self.__vector_3D:
            return Vector((self.x * other), (self.y * other), (self.z * other))
        return Vector((self.x * other), (self.y * other))
        
    def __rmul__(self, other) -> Vector:
        """
        Operation overloading for other * Vector.

        Args:
            other: The other variable (int/float/vector).

        Returns:
            A vector with the variables multiplied accordingly.
        """
        if isinstance(other, Vector):
            if self.__vector_3D:
                return Vector((other.x * self.x), (other.y * self.y), (other.z * self.z))
            return Vector((other.x * self.x), (other.y * self.y))
        if self.__vector_3D:
            return Vector((other * self.x), (other * self.y), (other * self.z))
        return Vector((other * self.x), (other * self.y))
    
    def __truediv__(self, other) -> Vector:
        """
        Operation overloading for Vector / other.

        Args:
            other: The other variable (int/float/vector).

        Returns:
            A vector with the variables divided accordingly.
        """
        if isinstance(other, Vector):
            if self.__vector_3D:
                return Vector((self.x / other.x), (self.y / other.y), (self.z / other.z))
            return Vector((self.x / other.x), (self.y / other.y))
        if self.__vector_3D:
            return Vector((self.x / other), (self.y / other), (self.z / other))
        return Vector((self.x / other), (self.y / other))
    
    def __rtruediv__(self, other) -> Vector:
        """
        Operation overloading for other / Vector.

        Args:
            other: The other variable (int/float/vector).

        Returns:
            A vector with the variables divided accordingly.
        """
        if isinstance(other, Vector):
            if self.__vector_3D:
                return Vector((other.x / self.x), (other.y / self.y), (other.z / self.z))
            return Vector((other.x / self.x), (other.y / self.y))
        if self.__vector_3D:
            return Vector((other / self.x), (other / self.y), (other / self.z))
        return Vector((other / self.x), (other / self.y))
        

    def __str__(self) -> str:
        """
        The string conversion of the Vector object.

        Returns:
            A readable string
        """
        if self.__vector_3D:
            return f'x = {self.x}, y = {self.y}, z = {self.z}'
        return f'x = {self.x}, y = {self.y}'
    
    def __repr__(self) -> str:
        """
        The string representation of the Vector object.

        Returns:
            A readable string
        """
        if self.__vector_3D:
            return f'{self.x}, {self.y}, {self.z}'
        return f'{self.x}, {self.y}'
    
    def __neg__(self) -> Vector:
        """
        The negative of the vector.

        Returns:
            A Vector that is the negative of the current Vector.
        """
        if self.__vector_3D:
            return Vector(-self.x, -self.y, -self.z)
        return Vector(-self.x, -self.y)
    
    @staticmethod
    def distance(first : Vector, second : Vector) -> float:
        """
        A method to calculate the distance between two vectors.

        Args:
            first: The first vector.
            second: The second vector.

        Returns:
            The distance between the two vectors.
        """
        if first.is3D() and second.is3D():
            return ((first.x - second.x) ** 2 + (first.y - second.y) ** 2 + (first.z - second.z) ** 2) ** 0.5
        elif not first.is3D() and not second.is3D():
            return ((first.x - second.x) ** 2 + (first.y - second.y) ** 2) ** 0.5
        else:
            raise TypeError("Both the Vectors should have same number of dimensions.")


            
    
def main() -> None:
    vector1 = Vector(1, 2, 3)
    print(vector1 / 2)
    print(2 / vector1)

if __name__ == "__main__":
    main()