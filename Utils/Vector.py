from __future__ import annotations

import math
    

class Vector():

    __vector_3D : bool
    
    def __init__(self, *args) -> None:
        
        if len(args) == 0:
            self.x = 0
            self.y = 0
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
        if not isinstance(other, Vector):
            if self.__vector_3D:
                self.x = (self.x + other)
                self.y = (self.y + other)
                self.z = (self.z + other)
            else:
                self.x = (self.x + other)
                self.y = (self.y + other)
        else:
            if self.__vector_3D:
                self.x = (self.x + other.x)
                self.y = (self.y + other.y)
                self.z = (self.z + other.z)
            else:
                self.x = (self.x + other.x)
                self.y = (self.y + other.y)

    def sub(self, other) -> None:
        if not isinstance(other, Vector):
            if self.__vector_3D:
                self.x = (self.x - other)
                self.y = (self.y - other)
                self.z = (self.z - other)
            else:
                self.x = (self.x - other)
                self.y = (self.y - other)
        else:
            if self.__vector_3D:
                self.x = (self.x - other.x)
                self.y = (self.y - other.y)
                self.z = (self.z - other.z)
            else:
                self.x = (self.x - other.x)
                self.y = (self.y - other.y)

    def divide(self, other) -> None:
        if not isinstance(other, Vector):
            if self.__vector_3D:
                self.x = (self.x / other)
                self.y = (self.y / other)
                self.z = (self.z / other)
            else:
                self.x = (self.x / other)
                self.y = (self.y / other)
        else:
            if self.__vector_3D:
                self.x = (self.x / other.x)
                self.y = (self.y / other.y)
                self.z = (self.z / other.z)
            else:
                self.x = (self.x / other.x)
                self.y = (self.y / other.y)

    def limit(self, limit : float):
        if self.__vector_3D:
            self.x = min(max(self.x, -limit), limit)
            self.y = min(max(self.y, -limit), limit)
            self.z = min(max(self.z, -limit), limit)
        else:
            self.x = min(max(self.x, -limit), limit)
            self.y = min(max(self.y, -limit), limit)

    def __add__(self, other) -> Vector:
        if not isinstance(other, Vector):
            if self.__vector_3D:
                return Vector((self.x + other), (self.y + other), (self.z + other))
            return Vector((self.x + other), (self.y + other))
        if self.__vector_3D:
            return Vector((self.x + other.x), (self.y + other.y), (self.z + other.z))
        return Vector((self.x + other.x), (self.y + other.y))
    
    def __sub__(self, other) -> Vector:
        if not isinstance(other, Vector):
            if self.__vector_3D:
                return Vector((self.x - other), (self.y - other), (self.z - other))
            return Vector((self.x - other), (self.y - other))
        if self.__vector_3D:
            return Vector((self.x - other.x), (self.y - other.y), (self.z - other.z))
        return Vector((self.x - other.x), (self.y - other.y))
    
    def __truediv__(self, other) -> Vector:
        if not isinstance(other, Vector):
            if self.__vector_3D:
                return Vector((self.x / other), (self.y / other), (self.z / other))
            return Vector((self.x / other), (self.y / other))
        if self.__vector_3D:
            return Vector((self.x / other.x), (self.y / other.y), (self.z / other.z))
        return Vector((self.x / other.x), (self.y / other.y))

    def __str__(self) -> str:
        if self.__vector_3D:
            return f'x = {self.x}, y = {self.y}, z = {self.z}'
        return f'x = {self.x}, y = {self.y}'
    
    def __repr__(self) -> str:
        if self.__vector_3D:
            return f'{self.x}, {self.y}, {self.z}'
        return f'{self.x}, {self.y}'
    
    def __neg__(self) -> Vector:
        if self.__vector_3D:
            return Vector(-self.x, -self.y, -self.y)
        return Vector(-self.x, -self.y)
    
    @staticmethod
    def distance(first : Vector, second : Vector) -> float:
        try:
            return math.sqrt((first.x - second.x) ** 2 + (first.y - second.y) ** 2 + (first.z - second.z) ** 2)
        except:
            return math.sqrt((first.x - second.x) ** 2 + (first.y - second.y) ** 2)


            
    
def main() -> None:
    vector1 = Vector(1, 2, 3)
    print(-vector1)

if __name__ == "__main__":
    main()