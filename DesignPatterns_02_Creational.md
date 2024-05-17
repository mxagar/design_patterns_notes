# Design Patterns: Creational Patterns

This document/guide is the second from a set of 4 documents:

1. SOLID Design Principles
2. **Creational Patterns**
3. Structural Patterns
4. Behavioral Patterns

See the overview file [`README.md`](README.md) for more information on the origin of the guides.

Creational patterns deal with the creation/construction of objects:

- The creation can be explicit (e.g., via constructors) of implicit (e.g., dependency injection, reflection, etc.).
- The creation can be wholesale (single statement creates the object) or piecewise, i.e., it is done step-by-step in a more complicated process.

Table of contents:

- [Design Patterns: Creational Patterns](#design-patterns-creational-patterns)
  - [1. Builder](#1-builder)
  - [2. Factories](#2-factories)
  - [3. Prototype](#3-prototype)
  - [4. Singleton](#4-singleton)

## 1. Builder

Sometimes objects are easy to create and they are built witha single initializer call. However, in some other cases creating an object is more complicated

- it requires several steps
- or it dozens of parameters are involved
- or a piecewise construction is required.

The **Builder** provides an API for constructing an object step-by-step: when piecewise object construction is complicated, it provides an API for doing it succinctly.

See notebook: [`Creational_Patterns.ipynb`](./02_Creational_Patterns/Creational_Patterns.ipynb).

Different examples are provided: 

- an HTML builder (in the notebook),
- a Car builder (below),
- a Person builder (in the notebook),
- and a Product builder (below). 

In general:

- We have an Object class and a Builder class which builds those objects.
- The Builder has methods that added components to the Object.
- We can either explicitly use the Builder or return it from the Object using a `create()` static method.
- We can make the builder fluent so that the methods that add components are chained.
- Different facets of an Object can be built with different Builder classes that work in tandem.
- We can define a Director class which `constructs()` different types of Objects.

**Car example**:

```python
class Car:
    def __init__(self):
        self.features = []

    def add_feature(self, feature):
        self.features.append(feature)

    def __str__(self):
        return ', '.join(self.features)

class CarBuilder:
    def __init__(self):
        self.car = Car()

    def add_engine(self, engine):
        self.car.add_feature(f"Engine: {engine}")
        return self

    def add_wheels(self, wheels):
        self.car.add_feature(f"Wheels: {wheels}")
        return self

    def add_gps(self):
        self.car.add_feature("GPS: Installed")
        return self

    def build(self):
        return self.car

class Director:
    def construct_sports_car(self, builder):
        return builder.add_engine('V8').add_wheels('Sports').add_gps().build()

    def construct_family_car(self, builder):
        return builder.add_engine('V4').add_wheels('Regular').add_gps().build()

# Usage
director = Director()
sports_car_builder = CarBuilder()
family_car_builder = CarBuilder()

sports_car = director.construct_sports_car(sports_car_builder)
family_car = director.construct_family_car(family_car_builder)

print(sports_car)  # Engine: V8, Wheels: Sports, GPS: Installed
print(family_car)  # Engine: V4, Wheels: Regular, GPS: Installed

```

**Product example**, taken from [All 23 OOP software design patterns with examples in Python](https://medium.com/@cautaerts/all-23-oop-software-design-patterns-with-examples-in-python-cac1d3f4f4d5):

- **Product**: This is the complex object under construction. It contains the parts that make up the product.

- **Builder**: The Builder defines the abstract interface for creating parts of the Product object. It declares the construction steps that are common to all types of builders. This allows the Director to construct products using any builder that implements this interface, without knowing the specific details of the construction process.

- **ConcreteBuilder**: The ConcreteBuilder implements the Builder interface and provides specific implementations for the construction steps. It keeps track of the product it creates and is responsible for assembling the parts into the final product. It knows the specifics of the parts it is supposed to create and how to assemble them.

- **Director**: The Director is responsible for managing the construction process. It uses a Builder instance to construct a product step-by-step. The Director doesn’t need to know the details of the product's construction, it only needs to ensure that the construction steps are followed in the correct order.

```python
from abc import ABC, abstractmethod
from typing import List

class Product:
   def __init__(self) -> None:
       self._parts: List[str] = []

   def add_part(self, part: str) -> None:
       self._parts.append(part)

   def get_parts(self) -> List[str]:
       return self._parts

class Builder(ABC):
    @abstractmethod
    def build_part_a(self) -> None:
        pass

    @abstractmethod
    def build_part_b(self) -> None:
        pass

    @abstractmethod
    def get_result(self) -> Product:
        pass

class ConcreteBuilder(Builder):
    def __init__(self) -> None:
        self.product = Product()

    def build_part_a(self) -> None:
        self.product.add_part("Part A")

    def build_part_b(self) -> None:
        self.product.add_part("Part B")

    def get_result(self) -> Product:
        return self.product

class Director:
    def __init__(self, builder: Builder) -> None:
        self._builder = builder

    def construct(self) -> None:
        self._builder.build_part_a()
        self._builder.build_part_b()

# Example usage
builder = ConcreteBuilder()
director = Director(builder)
director.construct()
product = builder.get_result()

print(product.get_parts())  # Output: ['Part A', 'Part B']

```

## 2. Factories

A Factory is a component responsible solely for the wholesale (not piecewise) creation of objects.

- Sometimes object creation logic becomes too convoluted.
- Class initialization with `__init__()` is indeed a bit limited:
  - Name is always `__init__()`.
  - Cannot be overloaded with same sets of arguments with different names
  - Can turn into an optional parameter hell.
- Solution: Factories - wholesale object creation (non-piecewise, i.e., not defined in steps, unlike Builder) that can be outsourced to
  - a set separate methods: **factory methods**;
  - that can may exist in a separate class **Factory**, which contains the factory methods;
  - And we can create a hierarchy of factories, i.e., **Abstract Factories**, which are factory classes created for abstract and derived object classes.

Notebook: [`Creational_Patterns.ipynb`](./02_Creational_Patterns/Creational_Patterns.ipynb)

In the notebook, two examples are shown to illustrate the abovementioned 3 concepts:

- Point class (summarized below): Factory Methods & Classes
- Hot drink class: Abstract Factory (in the notebook).

**Point example**:

```python
from enum import Enum
import math

class CoordinateSystem(Enum):
    CARTESIAN = 1
    POLAR = 2
    
class Point:
    # For the same point object
    # depending on a flag, the arguments
    # are treated differently
    # to deal with a more complex constructor.
    # (Recall in Python we cannot overload constructors).
    # BUT that's bad, because it complicates the usage
    # and everything is more confusing
    def __init__(self, a, b, system=CoordinateSystem.CARTESIAN):
        if system == CoordinateSystem.CARTESIAN:
            self.x = a
            self.y = b
        elif system == CoordinateSystem.POLAR:
            self.x = a * math.sin(b)
            self.y = a * math.cos(b)


# We create factory methods (static methods)
# inside the object Point class
# which deal with the correct coordinate system
# and return an object of the class itself!
class Point:
    def __init__(self, x, y):
       self.x = x
       self.y = y

    # Factory method 1
    @staticmethod
    def new_cartesian_point(x, y):
        return Point(x, y)

    # Factory method 2
    @staticmethod
    def new_polar_point(rho, theta):
        return Point(rho * math.sin(theta), rho * math.cos(theta))

    def __str__(self):
        return f'x: {self.x}, y: {self.y}'

# Usage
p1 = Point(2, 3, CoordinateSystem.CARTESIAN) # Extended constructor
p2 = Point.new_cartesian_point(1, 2) # Factory Method 1
p2 = Point.new_polar_point(3, 0.707) # Factory Method 2
print(p1)
print(p2)

# When we start having many factory methods
# it makes sense to build a class with all of them;
# that way, everything is more organized and clear.
# Since the Factory class is separate from the Object class
# if we want to make sure that it is not lost
# we can even include it into the object class itself
class Point:
    def __init__(self, x, y):
       self.x = x
       self.y = y

    def __str__(self):
        return f'x: {self.x}, y: {self.y}'

    class Factory:
        @staticmethod
        def new_cartesian_point(x, y):
            return Point(x, y)

        @staticmethod
        def new_polar_point(rho, theta):
            return Point(rho * math.sin(theta), rho * math.cos(theta))

# Usage
p4 = Point.Factory.new_polar_point(1, 0.5) # Object -> Factory Class -> Factory Method
print(p4)
```

## 3. Prototype

Prototype: We use them when it's easier to copy an existing object to fully initialize a new one. Thus, a Prototype is a partially or fully initialized object that we copy (*clone*) and make use of it:

- Complicated objects (e.g., cars) aren't designed from scratch.
  - They reiterate existing designs.
- An existing (partially or fully constructed) design is a Prototype.
- We want to copy it (*clone*), customize it, and start using it.
  - It requires a *deep copy* support, i.e., a wholesale copy.
  - Maybe the entire object is not created in the Prototype, but some parts only.
- We make the *cloning* convenient: e.g., via a Factory:
  - We define the Object class we'd like to clone.
  - We deine a Factory class for it.
  - In the Factory class, we partially construct some object templates.
  - For each object template, we create static factory methods.
  - Each static factory method clones == deep copies a template and customizes it.
  - We have a nice and easy API for the users that creates complex objects with few lines of code.

Notebook: [`Creational_Patterns.ipynb`](./02_Creational_Patterns/Creational_Patterns.ipynb).

```python
import copy

# Let's take the example of classes
# for which we would like to have already
# pre-conigured object instances
class Address:
    def __init__(self, street_address, city, country):
        self.country = country
        self.city = city
        self.street_address = street_address

    def __str__(self):
        return f'{self.street_address}, {self.city}, {self.country}'
    
class Employee:
    def __init__(self, name, address):
        self.address = address
        self.name = name

    def __str__(self):
        return f'{self.name} works at {self.address}'

# To build from prototypes, we define a factory
# which contains pre-configured templates of an object
class EmployeeFactory:
    # These are the prototypes which belong to the class,
    # i.e., the same for all class objects
    # since they are not defined in self
    main_office_employee = Employee("", Address("123 East Dr", 0, "London"))
    aux_office_employee = Employee("", Address("123B East Dr", 0, "London"))

    @staticmethod
    def __new_employee(proto, name, suite):
        result = copy.deepcopy(proto)
        result.name = name
        result.address.suite = suite
        return result

    @staticmethod
    def new_main_office_employee(name, suite):
        return EmployeeFactory.__new_employee(
            EmployeeFactory.main_office_employee,
            name, suite
        )

    @staticmethod
    def new_aux_office_employee(name, suite):
        return EmployeeFactory.__new_employee(
            EmployeeFactory.aux_office_employee,
            name, suite
        )

john = EmployeeFactory.new_aux_office_employee("John", 200)
jane = EmployeeFactory.new_main_office_employee("Jane", 200)
print(jane) # Jane works at 123 East Dr, 0, London
print(john) # John works at 123B East Dr, 0, London
```

## 4. Singleton

