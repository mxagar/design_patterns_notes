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
    - [Example: Geometric Shapes](#example-geometric-shapes)
    - [Example: Neural Networks](#example-neural-networks)
  - [4. Decorator](#4-decorator)
    - [Functional Decorators in Python: `@time_it`](#functional-decorators-in-python-time_it)
    - [(Classic) Class Decorator](#classic-class-decorator)
    - [Dynamic Class Decorator: `FileWithLogging`](#dynamic-class-decorator-filewithlogging)
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

Bridges connect components together through abstractions:

- A Bridge prevents a *Cartesian product* complexity explosion; example:
  - Base class `ThreadScheduler`
  - Can be pre-emptive or cooperative
  - Can run on Windows or Unix
  - We end-up having a 2x2 scenario: `WindowsPTS`, `UnixPTS`, `WindowsCTS`, `UnixCTS`
  - So, for each new dimension with levels we add, the number of classes explode, since all the levels need to be combined.
- The Bridge pattern avoids entity explosion.
- We don't rely on inheritance as much, instead, we use **inheritance + aggregation**.

Essentially, a Bridge is a mechanism that decouples an interface or abstraction (which can be a hierarchy) from an implementation (which can be another hierarchy), or in other words, it connects two hierarchies of different classes so that we don't need to performa Cartesian product of the class hierarchies. We can understand a Bridge as a stronger form of encapsulation.

The downside of the Bridge pattern is often that we break the Open-Close SOLID principle with it. However, that's the price we need to pay to avoid complexity explosion. When the Open-Close principle is broken, we need to modify many classes every time we add a new one.

```python
# We want to ender Circles and Squares: Circle, Square
# Each can be rendered in vector or raster form: Vector, Raster
# We could define these renderers:
# CircleVectorRender, CircleRasterRender, SquareVectorRender, SquareRasterRender
# But that doesn't make sense, the complexity explodes!
# To avoid that, we implement the Bridge pattern
# HOWEVER: Note that we break the Open-Close principle!
# That is the price we need to pay to avoid complexit explosion.
# Since the Open-Close principle is broken, whenever we add a new Shape,
# e.g., Triangle, we need to modify Renderer, VectorRenderer, RasterRenderer.
from abc import ABC, abstractmethod

# Abstract base class of the renderer
class Renderer(ABC):
    @abstractmethod
    def render_circle(self, radius):
        pass

    @abstractmethod
    def render_square(self, side):
        pass

# Vector Renderer inherits from base class and implements 2 shapes
# However, note that the render_ functions don't take a class (Circle, Square)
# but a parameter essential to defining the class (radius, side)!
class VectorRenderer(Renderer):
    def render_circle(self, radius):
        print(f'Drawing a circle of radius {radius}')

    def render_square(self, side):
        print(f'Drawing a square of side {side}')

# Raster Renderer inherits from base class and implements 2 shapes
# However, note that the render_ functions don't take a class (Circle, Square)
# but a parameter essential to defining the class (radius, side)!
class RasterRenderer(Renderer):
    def render_circle(self, radius):
        print(f'Drawing pixels for circle of radius {radius}')

    def render_square(self, side):
        print(f'Drawing pixels for a square of side {side}')

# THIS IS WHERE WE CREATE THE BRIDGE
# In a base class Shape we pass the Renderer as dependency/parameter!
# Then, we inherit concrete Shapes and each can take
# a Vector/ResterRenderer, which contain the methods for plotting each shape!
class Shape:
    def __init__(self, renderer):
        self.renderer = renderer

    def draw(self): pass
    def resize(self, factor): pass


class Circle(Shape):
    def __init__(self, renderer, radius):
        super().__init__(renderer)
        self.radius = radius

    def draw(self):
        self.renderer.render_circle(self.radius)

    def resize(self, factor):
        self.radius *= factor


class Square(Shape):
    def __init__(self, renderer, side):
        super().__init__(renderer)
        self.side = side

    def draw(self):
        self.renderer.render_square(self.side)

    def resize(self, factor):
        self.side *= factor

# __main__
raster = RasterRenderer()
vector = VectorRenderer()

circle = Circle(vector, 5)
circle.draw()
circle.resize(2)
circle.draw()

circle = Circle(raster, 5)
circle.draw()
circle.resize(2)
circle.draw()

square = Square(vector, 5)
square.draw()
square.resize(2)
square.draw()

square = Square(raster, 5)
square.draw()
square.resize(2)
square.draw()
```

## 3. Composite

The goal of a Composite is to treat individual/scalar and aggregate/collection objects uniformly:

- Objects use other object's properties/members through inheritance and composition.
- Composition lets us make compound objects.
  - Example: a mathematical expression composed of simple expressions or a grouping of shapes that consists of several shapes.
- **The Composite design pattern is used to treat both single (scalar) and composite objects uniformly.**
  - That is: a scalar/single object and a collection/sequence structure that containes those objects have common APIs.

Note: scalar is used here in the sense of a single object (e.g., a class or a object of a class), whereas group means a collection (e.g., a list).

The main difference between a scalar/single object and a group/collection object which can contain both the scalar/single objects and groups is **iteration**. Therefore, we need to somehow support iteration in the Composite:

- We can do that by defining the scalar objects as classes that contain iterables.
- Or we can also do that by defining the `__iter__` method in the scalar object.

### Example: Geometric Shapes

The Composite pattern allows to compose objects into tree structures to represent part-whole hierarchies. It lets clients treat individual objects and compositions of objects uniformly. Key components, focusing on the example of the **Geometric Shapes**:

- **Component**: The base class (`GraphicObject` in the example with the Geometric Shapes) represents both individual objects and their compositions.

- **Leaf**: The individual objects that can be part of a composition. In the following example, `Circle` and `Square` are leaf objects.

- **Composite**: The composite objects that can contain other objects. In the following example, `GraphicObject` itself acts as a composite that can contain other `GraphicObject` instances.

In the example of the Geometric Shapes, the coposite pattern is accomplised thanks to 3-4 key points:

- We define a member list which contains children: `self.children = []`
- We add derived class objects to the `children` list, as well as the `GraphicObject` type itsself, creating nested structures.
- We apply a recursive printing `_print` that traverses all the children and the children of the children; that's a depth-first tree traverse.

```python
# This base class can be 2 things:
# a single shape (derived) or a group/collection of shapes
class GraphicObject:
    def __init__(self, color=None):
        self.color = color
        self.children = [] # Key line for Composite
        self._name = 'Group' # We will override the name in inherited shapes

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    # We create a list of ObjectColor items
    # preceeded by the depth represented with the number of *
    # This recursive function is a tree traverse
    # and it's a key part of the Composite pattern
    def _print(self, items, depth):
        items.append('*' * depth)
        if self.color:
            items.append(self.color)
        items.append(f'{self.name}\n')
        for child in self.children:
            child._print(items, depth + 1)

    def __str__(self):
        items = []
        self._print(items, 0)
        return ''.join(items)


class Circle(GraphicObject):
    @property
    def name(self):
        return 'Circle'


class Square(GraphicObject):
    @property
    def name(self):
        return 'Square'

# __main__
drawing = GraphicObject()
#drawing._name = 'My Drawing'
drawing.name = 'My Drawing'
# Key line for Composite: we add a derived class object
drawing.children.append(Square('Red'))
drawing.children.append(Circle('Yellow'))

group = GraphicObject()  # no name
group.children.append(Circle('Blue'))
group.children.append(Square('Blue'))
# Key line for Composite: we add an object of the Composite class itself
# creatiga nested structure
drawing.children.append(group) # we are appending a group to it!

# The composite pattern is used here!
# With a simple print() that uses __str__
# the complete tree structure consisting of leaf objects
# and group/composite objects is traversed and printed!
print(drawing)
```

### Example: Neural Networks

This is a very interesting case of the Composite pattern in which a function/method that should work the same way for a scalar object (`Neuron`) and a collection of it (`NeuronLayer`), i.e., `connect_to`, is implemented in a bas class `Connectable` from which `Neuron` and `NeuronLayer` are derived. Additionally, we add `__iter__` to the scalar class (`Neuron`) so that it can be iterable in a for loop, as well as the collection (`NeuronLayer`).

```python
from abc import ABC
from collections.abc import Iterable

# A straightforward class for a Neuron
# and a Neuron Layer
class Neuron():
    def __init__(self, name):
        self.name = name
        self.inputs = []
        self.outputs = []

    def connect_to(self, other):
        self.outputs.append(other)
        other.inputs.append(self)

    def __str__(self):
        return f'{self.name}, {len(self.inputs)} inputs, {len(self.outputs)} outputs'

class NeuronLayer(list):
    def __init__(self, name, count):
        super().__init__()
        self.name = name
        for x in range(0, count):
            self.append(Neuron(f'{name}-{x}'))

    def __str__(self):
        return f'{self.name} with {len(self)} neurons'
    
# However, this classes as they are defined
# make it difficult to perform the following operations
#   neuron1.connect_to(neuron2)
#   neuron1.connect_to(layer1)
#   layer1.connect_to(neuron2)
#   layer1.connect_to(layer2)
# 
# That is difficult, because we would have to implement
# different connect_to methods, where the types are checked.
# Instead, we use the Composite pattern

# We define this class _only_ to share the 
# function connect_to with any other class which is inherited with it
class Connectable(Iterable, ABC):
    def connect_to(self, other):
        if self == other: # cannot connect to yourself
            return

        for s in self:
            for o in other:
                s.outputs.append(o)
                o.inputs.append(s)

# Since Neuron is inherited from Connectable, 
# it has the connect_to method!
class Neuron(Connectable):
    def __init__(self, name):
        self.name = name
        self.inputs = []
        self.outputs = []

    # With this function we turn a scalar value into a collection of 1
    # We need it because connect_to expects a collection in the for-loop!
    def __iter__(self):
        yield self

    def __str__(self):
        return f'{self.name}, {len(self.inputs)} inputs, {len(self.outputs)} outputs'

# Since NeuronLayer is inherited from Connectable, 
# it has the connect_to method!
class NeuronLayer(list, Connectable):
    def __init__(self, name, count):
        super().__init__()
        self.name = name
        for x in range(0, count):
            self.append(Neuron(f'{name}-{x}'))

    def __str__(self):
        return f'{self.name} with {len(self)} neurons'

# __main__

neuron1 = Neuron('n1')
neuron2 = Neuron('n2')
layer1 = NeuronLayer('L1', 3)
layer2 = NeuronLayer('L2', 4)

neuron1.connect_to(neuron2)
neuron1.connect_to(layer1)
layer1.connect_to(neuron2)
layer1.connect_to(layer2)

print(neuron1)
print(neuron2)
print(layer1)
print(layer2)
```

## 4. Decorator

With a Decorator we add behavior to a class/function without altering it itself or without inheriting it.

Motivation:

- We want to augment an object with additional functionality.
- We don't want to break the Open-Close principle, and we don't want to alter any existing code.
- We want to keep the new functionality separate (Single Responsibility Principle).
- We need to be able to interact with existing structures.
- We have 2 main options:
  - Inherit from required object (if possible).
  - Build a Decorator, which simply references the decorated object(s).

Decorators in Python are built-in, but as rather as functional decorators, not as general purpose decorators, as defined in this section.

### Functional Decorators in Python: `@time_it`

```python
import time

# A (built-in) Python decorator is defined as a wrapper function
# which takes a function as an argument
# and an action is performed with that function
def time_it(func):
    def wrapper():
        start = time.time()
        result = func()
        end = time.time()
        print(f'{func.__name__} took {int((end-start)*1000)}ms')
    return wrapper

@time_it # equivalent: time_it(some_op())
def some_op():
    print('Starting op')
    time.sleep(1)
    print('We are done')
    return 123

# __main__
# time_it(some_op)() # equivalent call
some_op()
```

### (Classic) Class Decorator

The folowing example shows the classic class decorator, which works by defining a class which takes an underlying object and extends it with decorating functionality. However, it has two major problems:

- We loose access to the underlying object structure!
- Nothing prevents us from using the decorator more than once, which is not correct!

```python
from abc import ABC, abstractmethod


# Abstract class, to be inherited and implemented
class Shape(ABC):
    @abstractmethod
    def __str__(self):
        return ''

# Concrete class 1
class Circle(Shape):
    def __init__(self, radius=0.0):
        self.radius = radius

    def resize(self, factor):
        self.radius *= factor

    def __str__(self):
        return f'A circle of radius {self.radius}'

# Concrete class 2
class Square(Shape):
    def __init__(self, side):
        self.side = side
        
    def resize(self, factor):
        self.side *= factor

    def __str__(self):
        return f'A square with side {self.side}'

# Decorator class 1
# This is like a decorator because
# we add color to any shape
# IMPORTANT: ColoredShape is inherited from Shape!
class ColoredShape(Shape):
    def __init__(self, shape, color):
        if isinstance(shape, ColoredShape):
            raise Exception('Cannot apply ColoredDecorator twice')
        self.shape = shape
        self.color = color

    def __str__(self):
        return f'{self.shape} has the color {self.color}'

# Decorator class 2
# This is like a decorator because
# we add transparency to any shape
# IMPORTANT: TransparentShape is inherited from Shape!
class TransparentShape(Shape):
    def __init__(self, shape, transparency):
        self.shape = shape
        self.transparency = transparency

    def __str__(self):
        return f'{self.shape} has {self.transparency * 100.0}% transparency'

# __main__
circle = Circle(2)
print(circle)

# Since Circle is inherited from Shape
# we can use it with ColoredShape!
# This s like a decorator
red_circle = ColoredShape(circle, "red")
print(red_circle)

# Since ColoredShape is inherited from Shape
# we can use it with TransparentShape!
# This is like a decorator
red_half_transparent_square = TransparentShape(red_circle, 0.5)
print(red_half_transparent_square)

# PROBLEM #1: 
# ColoredShape doesn't have resize(), as Circle and Square,
# i.e., we cannot access the underlying object!
red_circle.resize(3) # AttributeError!

# PROBLEM #2:
# Nothing prevents double application!
mixed = ColoredShape(ColoredShape(Circle(3), 'red'), 'blue') # Exception!
```

### Dynamic Class Decorator: `FileWithLogging`

Dynamic class decorators alleviate the major problem of the classic class decorators: the underlying object becomes inaccessible.

In the following example, `FileWithLogging` is implemented, where a `File` object is passed as unique attribute; i.e., `FileWithLoging` is the decorator and it keeps a reference to the object it decorates: `File`. Then, the API of `File` is re-implemented inside `FileWithLogging` by adding extra logging functionalities. In that process, `File` is not really modified, but we build a wrapper around it.

Thus, basically, the Decorator re-implements the complete class API by adding extra functionality. Note: maybe we don't need to re-implement the complete API, but the functions/methods we know we're going to use!

```python
class FileWithLogging:
    def __init__(self, file):
        self.file = file

    def writelines(self, strings):
        self.file.writelines(strings)
        # This is the logging functionality we add
        print(f'wrote {len(strings)} lines')

    # So that it works, we need to overwrite all
    # the methods of a file handler...
    def __iter__(self):
        return self.file.__iter__()

    def __next__(self):
        return self.file.__next__()

    def __getattr__(self, item):
        # We get the file object/attribute using __dict__
        # because that way we don't rely on how it is implemented:
        # If the file attribute in the FileWithLogging class 
        # or its parent classes is implemented as a descriptor 
        # (e.g., using property), the direct attribute access version 
        # will invoke the descriptor's methods, 
        # whereas the dictionary access version will not.
        # Direct attribute access might be slightly slower 
        # than dictionary access due to the additional steps 
        # involved in the attribute lookup process,
        # such as checking for descriptors. 
        # However, this difference is usually negligible.
        return getattr(self.__dict__['file'], item)

    def __setattr__(self, key, value):
        if key == 'file':
            self.__dict__[key] = value
        else:
            setattr(self.__dict__['file'], key)

    def __delattr__(self, item):
        delattr(self.__dict__['file'], item)

# __main__
file = FileWithLogging(open('hello.txt', 'w'))
file.writelines(['hello', 'world'])
file.write('testing') # wrote 2 lines
file.close()
```

## 5. Facade

TBD.

## 6. Flyweight

TBD.

## 7. Proxy

TBD.

