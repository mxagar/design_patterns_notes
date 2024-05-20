# Design Patterns: Structural Patterns

This document/guide is the third from a set of 4 documents:

1. SOLID Design Principles
2. Creational Patterns
3. **Structural Patterns**
4. Behavioral Patterns

See the overview file [`README.md`](README.md) for more information on the origin of the guides.

In the present guide, the **Structural Patterns** are defined and examples are given.

Structural patterns deal with the structure of objects:

- Class members, adherence to interfaces, etc.
- Many patterns are wrappers that mimic the underlying class interface.
- Stress the importance of good API design: usability, etc.

Table of Contents:

- [Design Patterns: Structural Patterns](#design-patterns-structural-patterns)
  - [1. Adapter](#1-adapter)
    - [Adapter: Point and Line Example](#adapter-point-and-line-example)
    - [Adapter with Caching](#adapter-with-caching)
  - [2. Bridge](#2-bridge)
  - [3. Composite](#3-composite)
  - [4. Decorator](#4-decorator)
  - [5. Facade](#5-facade)
  - [6. Flyweight](#6-flyweight)
  - [7. Proxy](#7-proxy)

## 1. Adapter

An analogy of the Adapter are the physical power adapters:

- The devices have different power requirements: 5V, 220V, 120V, plug type EU/US, etc.
- We cannot modify our gadgets to support every possible interface!

An adapter is a construct which adapts an existing interface X to conform the required interface Y.

### Adapter: Point and Line Example

This example shows the interplay between a Point, Line and Rectangle class. The goal is to draw all the discrete Points of a Rectangle. To that end, we adapt the Line class (which is defined with start and end Points) to deliver all the discrete Points in it.

```python
# Let's suppose we are given a class Point
# and a function draw_point
class Point:
    def __init__(self, x: int, y: int):
        self.y = y
        self.x = x


def draw_point(p):
    print('.', end='')


# Then, we build two more classes: Line and Rectangle
# Both consist of Point elements in discrete coordinates
# and we would like to draw all the points in a Rectangle
# or a Line
class Line:
    def __init__(self, start, end):
        self.end = end
        self.start = start


class Rectangle(list):
    """ Represented as a list of lines. """

    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__()
        self.append(Line(Point(x, y), Point(x + width, y)))
        self.append(Line(Point(x + width, y), Point(x + width, y + height)))
        self.append(Line(Point(x, y), Point(x, y + height)))
        self.append(Line(Point(x, y + height), Point(x + width, y + height)))


# We want to draw the rectangles
# But: rectangles consist of lines, which consist of points
# and we want to use the draw_point function,
# which draws a unique point each call.
# We need a LineToPointAdapter, which converts a Line
# defined with its start and end points to a set of points
# lying between the start and end points
def draw(rcs):
    print("\n\n--- Drawing some stuff ---\n")
    for rc in rcs:
        for line in rc:
            # We need a LineToPointAdapter!
            pass


# A Line is defined with a start and an end point
# This adapter converts the line to a set of Points
# between the start and end (included).
class LineToPointAdapter(list):
    count = 0

    def __init__(self, line):
        super().__init__()
        self.count += 1
        print(f'{self.count}: Generating points for line '
              f'[{line.start.x},{line.start.y}]-->'
              f'[{line.end.x},{line.end.y}]')

        left = min(line.start.x, line.end.x)
        right = max(line.start.x, line.end.x)
        top = min(line.start.y, line.end.y)
        bottom = min(line.start.y, line.end.y)

        # Since we are dealing with rectangles
        # lines can be either vertical or horizontal
        if right - left == 0:
            # Point and Line consist of int coordinates
            # thus, range works
            for y in range(top, bottom):
                self.append(Point(left, y))
        elif line.end.y - line.start.y == 0:
            for x in range(left, right):
                self.append(Point(x, top))



def draw(rcs):
    print("\n\n--- Drawing some stuff ---\n")
    for rc in rcs:
        for line in rc:
            adapter = LineToPointAdapter(line)
            for p in adapter:
                draw_point(p)


# __main__
rs = [
    Rectangle(1, 1, 10, 10),
    Rectangle(3, 3, 6, 6)
]
draw(rs)
draw(rs)
```

### Adapter with Caching

Adapters often lead to too many temporary objects which are re-generared once and again. To alleviate that innecessary effort, we can add a cache dictionary to our adapter.

```python
# We add a caching dictionary to the Adapter
# to avoid re-generating too many temporary objects
# Note that it's not inherited from a list
# because the information is saved in the cache dict!
class LineToPointAdapter:
    cache = {}

    def __init__(self, line):
        self.h = hash(line) # Compute the hash of the line = key
        # Note: hash() works in two cases:
        # - if the input is inmutable: int, float, string, etc.
        # - if the input us mutable (list, class, etc.) it needs to have the __hash__ method implemented
        if self.h in self.cache:
            # Set of generated points is already in the cache!
            return

        # If the hash doesnt exist, the points were not generated
        # thus, we need to generate them
        super().__init__()
        print(f'Generating points for line ' +
              f'[{line.start.x},{line.start.y}]-->[{line.end.x},{line.end.y}]')

        left = min(line.start.x, line.end.x)
        right = max(line.start.x, line.end.x)
        top = min(line.start.y, line.end.y)
        bottom = min(line.start.y, line.end.y)

        # List of points to store = value
        points = []

        if right - left == 0:
            for y in range(top, bottom):
                points.append(Point(left, y))
        elif line.end.y - line.start.y == 0:
            for x in range(left, right):
                points.append(Point(x, top))

        # Store key-value pair in dict
        self.cache[self.h] = points

    # Beforehand, we LinetoPointAdapter was inherited from a list
    # Now, everything is in a dict
    # Thus, we implement the dunder method __iter__
    # to make possible iterating like in a list
    def __iter__(self):
        return iter(self.cache[self.h])

# Same as before
def draw(rcs):
    print('Drawing some rectangles...')
    for rc in rcs:
        for line in rc:
            adapter = LineToPointAdapter(line)
            for p in adapter:
                draw_point(p)
    print('\n')

# __main__
rs = [
    Rectangle(1, 1, 10, 10),
    Rectangle(3, 3, 6, 6)
]

draw(rs)
draw(rs)

# Can define your own hashes or use the defaults
# Note: hash() works in two cases:
# - if the input is inmutable: int, float, string, etc.
# - if the input us mutable (list, class, etc.) it needs to have the __hash__ method implemented
# In our case, Line is a list
print(hash(Line(Point(1, 1), Point(10, 10)))) # 99894889213
```

## 2. Bridge

TBD.

## 3. Composite

TBD.

## 4. Decorator

TBD.

## 5. Facade

TBD.

## 6. Flyweight

TBD.

## 7. Proxy

TBD.

