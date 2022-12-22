class Rectangle:
    def __init__(self, width, height):
        # We add _ to signal that these are private
        # Then, we define getters and setters
        self._height = height
        self._width = width

    @property
    def area(self):
        return self._width * self._height

    def __str__(self):
        # Note that self.width is calling self.width()
        # via the @property decorator
        return f'Width: {self.width}, height: {self.height}'

    # Property decorator: getter for width
    # Note: same name without _
    # Thus, we can now do object.width
    # and that calls object.width()
    # Using this strategy makes possible to handle
    # unit conversions, etc.
    @property
    def width(self):
        return self._width

    # Setter of the property.
    # Thus we can do now object.width = value
    # and that calls object.width(value)
    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

# Now, we inherit Square from Rectangle
class Square(Rectangle):
    def __init__(self, size):
        Rectangle.__init__(self, size, size)

    # We call the setter of the Rectangle parent class
    @Rectangle.width.setter
    def width(self, value):
        self._width = self._height = value

    @Rectangle.height.setter
    def height(self, value):
        self._width = self._height = value

if __name__ == "__main__":
        
    # This function breaks the Liskov substitution principle.
    # According to the principle, if we use an inheritec class of Rectangle,
    # i.e., Square, the function should work.
    # However, it doesn't work, because Square re-assings the width when the height
    # is modified.
    # Possible solutions:
    # - Do not create a Square class inherited from Rectangle: use Rectangle instead, maybe with a bool isSquare.
    # - We can use factories also, introduced later.
    def use_it(rc):
        w = rc.width
        rc.height = 10  # unpleasant side effect
        expected = int(w * 10)
        print(f'Expected an area of {expected}, got {rc.area}')

    # 
    rc = Rectangle(2, 3)
    use_it(rc)

    sq = Square(5)
    use_it(sq)
