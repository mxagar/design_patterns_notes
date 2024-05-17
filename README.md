# Notes on Design Patterns in Python

This guide and its related files were created while following the Udemy courses

- [Design Patterns in Modern C++](https://www.udemy.com/course/patterns-cplusplus/)
- [Design Patterns in Python](https://www.udemy.com/course/design-patterns-python/)

by Dmitri Nesteruk. I use some C++ examples, by I try to **focus primarily in Python**.

I found a repository by Dmitri Nesteruk, which I forked

- [https://github.com/mxagar/DesignPatternsWebinar](https://github.com/mxagar/DesignPatternsWebinar)
- [https://github.com/nesteruk/DesignPatternsWebinar](https://github.com/nesteruk/DesignPatternsWebinar)

However, the current repository builds up on that one and re-structures the complete code. Nevertheless, note that the original example code is by Dmitri Nesteruk.

In addition to the aforementioned courses, I also used the following resources:

- "Design Patterns" (Addison Wesley), by Gamma, Helm, Johnson & Vlissides (The Gang of Four)
- "Design Patterns" (O'Reilly Head First), by Kathy Sierra and Bert Bates
- [Python Design Patterns, by Brandon Rhodes](https://python-patterns.guide/)

The notes are divided into the following documents:

- [`DesignPatterns_01_SOLID.md`](DesignPatterns_01_SOLID.md)
- [`DesignPatterns_02_Creational.md`](DesignPatterns_02_Creational.md)
- [`DesignPatterns_03_Structural.md`](DesignPatterns_03_Structural.md)
- [`DesignPatterns_04_Behavioral.md`](DesignPatterns_04_Behavioral.md)

And the code with examples is located in their corresponding folders:

- [`01_SOLID/`](01_SOLID)
- [`02_Creational_Patterns/`](02_Creational_Patterns)
- [`03_Structural_Patterns/`](03_Structural_Patterns)
- [`04_Behavioral_Patterns`](04_Behavioral_Patterns)

Finally, note that knowledge and experience in Object Oriented Programming (OOP) is required to use this guide; a short summary on OOP using Python is given in the section [Object Oriented Programming](#object-oriented-programming-oop).

Table of contents:

- [Notes on Design Patterns in Python](#notes-on-design-patterns-in-python)
  - [What Are Design Patterns?](#what-are-design-patterns)
  - [Installation](#installation)
    - [C++](#c)
    - [Python](#python)
  - [Object Oriented Programming (OOP)](#object-oriented-programming-oop)
  - [Interesting Links and Resources](#interesting-links-and-resources)
  - [Authorship](#authorship)


## What Are Design Patterns?

Design Patterns are common and re-usable programming approaches that were popularized in the book of the same name (by "the Gang of Four": Gamma, Helm, Johnson & Vlissides).
They have been internalized to some languages and every programmer should know them, since they are the basic vocabulary and grammar for software architecture.

According to the Gamma categorization (Erich Gamma, from the Gang of Four), there are three types of patterns:

1. Creational
2. Structural
3. Behavioral

This guide compiles all the patterns defined in the book by the Gang of Four and additionally introduces the SOLID principles:

1. **SOLID Design Principles**

- Single Responsibility
- Open-Closed
- Liskov Substitution
- Interface Segregation
- Dependency Inversion

1. **Creational Patterns**

Creational patterns deal with the creation/construction of objects:

- The creation can be explicit (e.g., via constructors) of implicit (e.g., dependency injection, reflection, etc.).
- The creation can be wholesale (single statement creates the object) or piecewise, i.e., it is done step-by-step in a more complicated process.

Patterns:

- Builder
- Factories: Abstract, Factory Method
- Prototype
- Singleton

1. **Structural Patterns**

Structural patterns deal with the structure of objects:

- Class members, adherence to interfaces, etc.
- Many patterns are wrappers that mimic the underlying class interface.
- Stress the importance of good API design: usability, etc.

Patterns:

- Adapter
- Bridge
- Composite
- Decorator
- Facade
- Flyweight
- Proxy

1. **Behavioral Patterns**

Behavioral patterns don't really follow any central theme:

- They are all different.
- Sometimes they overlap in their function, i.e., the goal they achieve, but the underlying mechanisms are different.
  
Patterns:

- Chain of Responsibility
- Command
- Interpreter
- Iterator
- Mediator
- Memento
- Observer
- State
- Strategy
- Template Method
- Visitor

Nesteruk warns that, for the sake of simplicity, there are some simplifications in his examples: liberal use of public members, lack of virtual destructors, passing/returning by value, lack of move operations...

## Installation

I use both Python and C++ in the notes and code examples, but I focus primarily on Python.

### C++

The [boost](https://www.boost.org/) libraries are used throughout the course. To install them on a Mac:

```bash
brew install boost
```

Additionally, the `CMakeLists.txt` file of each project needs to be updated to contain all necessary Boost library information:

```cmake
list(APPEND CMAKE_PREFIX_PATH /opt/homebrew)
find_package(Boost REQUIRED)
include_directories(${Boost_INCLUDE_DIR})

add_executable(main main.cpp)
target_link_libraries(main ${Boost_LIBRARIES})
```

### Python

No preliminary installations needed; concrete installations introduced in specific example explanations, if needed.

I use `conda` environments.

## Object Oriented Programming (OOP)

This repository assumes you have experience in Object-Oriented Programming (OOP). Here's a reminder of the most important concepts in Python.

- Classes and objects
  - Constructor
  - Attributes (i.e., state)
  - Methods
- Encapsulation: public and private data and methods, grouped together; properties, getters and setters.
- Inheritance: classes (children) derived from other classes (parents); `is-a` relationships.
- Composition: complex objects built using other objects; class built using other classes, i.e. `has-a` relationships.
- Mixin: we inherit a class from two, they allow for the implementation of specific functionalities to be shared across multiple classes.
- Interfaces: classes with non-implemented methods, i.e., kind of contracts that define which methods should be implemented in the inherited classes. In Python, interfaces can be defined using abstract base classes (`from abc import ABC, abstractmethod`) with abstract methods, i.e., using `@abstractmethod`. An abstract method **needs** to be defined in the derived class, otherwise the `TypeError ` is raised at the moment we attempt to create an instance of the subclass.
- Polymorfism: when a function accepts objects of different classes because they all come from the same parent class; ability of different types of objects to be treated as instances of the same class through inheritance.
- Abstraction: writing code at higher level hiding details; polymorfism is an example: interfaces don't know anything about the underlying implementation but we use them to pass objects to functions!
- Dependency Injection: passing one object into another object's methods or constructor, instead of creating it internally.
- Mocking: passing a minimal implementation that adheres to correct interfaces/signatures for the purpose of testing.
- Static methods via `@staticmethod`: methods that don't change the object, usually they don't access class attributes.
- Abstract methods : 
- Class methods via `@classmethod`: an attribute of the *class* is modified, i.e., same value for all class object instances.
- Caching via `@functools.lru_cache`: memoization utility, i.e., results of expensive functions (e.g., recursive) are cached in a dictionary.
- Overloading via `@functools.singledispatch`: different behaviors allowed for the same function signature depending on the type of the arguments.
- Some other additional points:
  - Type hints
  - Keywords like `pass` and ellipsis `...`
  - Error/exception raising
  - `Enum`
  - Fluent interfaces with chaineable calls
  - Deep copies

Python examples:

```python
##### -- Classes, Objects, Attributes, Methods, Constructors, Encapsulation
class Person:
    def __init__(self, name, id=None):
        if id is None:
            id = uuid.uuid4()
        # In Python all members are public
        # but as convention to denote one to be used as private
        # we can use a leading _
        self._name = name
        # If we precede a class attribute with __
        # Python carries out name mangling, so the variable
        # is even more difficult to be accessed,
        # i.e., it seems to be really private.
        # However, it is really still accessible via
        # object._ClassName__variableName
        self.__id = id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def id(self):
        return self.__id  


person = Person("Alice")
print(person.name)  # Output: Alice
person.name = "Bob"
print(person.name)  # Output: Bob
print(person.id)  # Output: The UUID value (e.g., 123e4567-e89b-12d3-a456-426614174000)
# Accessing the private variable via name mangling
print(person._Person__id)  # Output: The same UUID value as above


##### -- Inheritance
class Employee(Person):
    def __init__(self, name, employee_id):
        super().__init__(name)
        self.employee_id = employee_id


##### -- Composition
class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, employee):
        if isinstance(employee, Employee):
            self.employees.append(employee)

dept = Department("HR")
dept.add_employee(Employee("Jane Doe", "1234"))


##### -- Mixin
class JsonMixin:
    """Mixin to add JSON serialization functionality to a class."""
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Student(JsonMixin, Person):
    def __init__(self, name, age, school):
        super().__init__(name, age)
        self.school = school

student = Student('John Doe', 20, 'MIT')
print(student.to_json())


##### -- Interfaces, Polymorphism and Abstraction
from abc import ABC, abstractmethod

# If we don't inherit from ABC the implementation
# of the @abstractmethods is not enforced in subclasses
# and we loose automatic checks from ABC -- but it still works!
class MyInterface(ABC):
    @abstractmethod
    def needed_method(self) -> str:
        pass

class ConcreteImplementationA(MyInterface):
    def needed_method(self) -> str:
        return "concrete_a"

class ConcreteImplementationB(MyInterface):
    def needed_method(self) -> str:
        return "concrete_b"

def polymorphic_function(obj: MyInterface) -> None:
    print(obj.needed_method())

a = ConcreteImplementationA()
b = ConcreteImplementationB()
polymorphic_function(a)
polymorphic_function(b)


##### -- Dependency Injection
class Logger:
    def log(self, message):
        print(f"Log: {message}")

class Application:
    def __init__(self, logger):
        self.logger = logger

    def do_something(self):
        self.logger.log("Something was done")

app = Application(Logger())
app.do_something()


##### -- Mocking
class MockLogger:
    def log(self, message):
        print(f"Mock log: {message}")

test_app = Application(MockLogger())
test_app.do_something()


##### -- Static Methods
class MathOperations:
    @staticmethod
    def add(x, y):
        return x + y

##### -- Class Methods
class Person:
    population = 0
    def __init__(self, name):
        self.name = name
        Person.population += 1
    
    @classmethod
    def how_many(cls):
        return cls.population


##### -- Caching 
import functools

class Fibonacci:
    @staticmethod
    @functools.lru_cache(maxsize=None)  # Cache results indefinitely
    def fib(n):
        if n < 2:
            return n
        return Fibonacci.fib(n-1) + Fibonacci.fib(n-2)


##### -- Overloading
from functools import singledispatch

@singledispatch
def say_hello(value):
    print(f"Hello {value}!")

@say_hello.register(int)
def _(value):
    print(f"Hello from a number: {value}!")

@say_hello.register(list)
def _(value):
    print("Hello from a list!")
    for item in value:
        print(f"- {item}")

##### -- Type Hints
def greet(name: str) -> str:
    return f"Hello, {name}!"

##### -- Pass
class MyAbstractClass:
    def do_something(self):
        pass  # No operation here

def unimplemented_function():
    ...  # Another placeholder, functionally similar to 'pass' in this context

my_object = MyAbstractClass()
my_object.do_something()  # Does nothing
unimplemented_function()  # Also does nothing

##### -- Enum
from enum import Enum, auto

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

favorite_color = Color.RED
print(favorite_color)  # Outputs: Color.RED
print(favorite_color.name, favorite_color.value)  # Outputs: RED 1

# With auto() we don't need to assign a value
class Drink(Enum):
    COFFEE = auto()
    TEA = auto()
    JUICE = auto()
    WATER = auto()

##### -- Error handling
def divide(x: int, y: int) -> float:
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y

try:
    result = divide(10, 0)
except ValueError as e:
    print(e)  # Outputs: Cannot divide by zero.

##### -- Fluent interfaces
class Car:
    def __init__(self):
        self.color = None
        self.brand = None

    def set_color(self, color):
        self.color = color
        return self  # Return self to allow chaining

    def set_brand(self, brand):
        self.brand = brand
        return self  # Return self to allow chaining

    def __str__(self):
        return f"Car(Brand={self.brand}, Color={self.color})"

# Usage
my_car = Car().set_color('red').set_brand('Toyota')
print(my_car)  # Outputs: Car(Brand=Toyota, Color=red)

##### -- Deep copies
import copy

car_vw = Car().set_color('red').set_brand('VW')
car_vw_2 = car_vw # This is not a real copy! Car is mutable, so we assign a pointer!
car_vw_3 = copy.deepcopy(car_vw) # This is a real copy, new bytes in memory!

```

## Interesting Links and Resources

- [All 23 OOP software design patterns with examples in Python](https://medium.com/@cautaerts/all-23-oop-software-design-patterns-with-examples-in-python-cac1d3f4f4d5)
- [SOLID Principles In Python](https://medium.com/@umaparvat/solid-principles-in-python-c9c3c337e0e1)
- [Python Design Patterns In Real World Projects](https://medium.com/python-in-plain-english/python-design-patterns-in-real-world-projects-%EF%B8%8F-ffedfe30330b)
- [Architecture Patterns: The Cheat Sheet](https://medium.com/scub-lab/architecture-patterns-the-cheat-sheet-e8b5386f4b4b)
- [It All Comes Down To Design Patterns](https://towardsdatascience.com/it-all-comes-down-to-design-patterns-c7034eb39ef9)
- [Refactoring Guru: Design Patterns](https://refactoring.guru/design-patterns)
- [Design Patterns Quick Reference by Jason McDonald](http://www.mcdonaldland.info/2007/11/28/40/)

## Authorship

Original code and examples primarily from from Dmitri Nesteruk.

Code modifications and notes: Mikel Sagardia, 2022.  
No guaranties.
