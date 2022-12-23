# Design Patterns: SOLID Design Principles

This document/guide is the first from a set of 4 documents:

1. **SOLID Design Principles**
2. Creational Patterns
3. Structural Patterns
4. Behavioral Patterns

See the overview file [`README.md`](README.md) for more information on the origin of the guides.

In the present guide, the **SOLID Design Principles** are defined and examples are given. The SOLID Design Principles were introduced by Robert C. Martin (Uncle Bob), known also for the Agile Manifesto.

Table of Contents:

- [Design Patterns: SOLID Design Principles](#design-patterns-solid-design-principles)
  - [1. Single Responsibility Principle (SRP): `01_SOLID/SRP.cpp`](#1-single-responsibility-principle-srp-01_solidsrpcpp)
    - [Python Implementation](#python-implementation)
  - [2. Open-Closed Principle: `01_SOLID/OCP.cpp`](#2-open-closed-principle-01_solidocpcpp)
    - [Python Implementation](#python-implementation-1)
  - [3. Liskov Substitution Principle: `01_SOLID/LSP.cpp`](#3-liskov-substitution-principle-01_solidlspcpp)
    - [Python Implementation](#python-implementation-2)
  - [4. Interface Segregation Principle: `01_SOLID/ISP.cpp`](#4-interface-segregation-principle-01_solidispcpp)
    - [Python Implementation](#python-implementation-3)
  - [5. Dependency Inversion Principle: `01_SOLID/DIP.cpp`](#5-dependency-inversion-principle-01_soliddipcpp)

## 1. Single Responsibility Principle (SRP): `01_SOLID/SRP.cpp`

A class should take one responsibility, and only one. That way, we are going to have only one reason to change it. The principle is also known as **Separation of Concerns (SOC)**: we assign clear concerns to specific classes.

The example used in the tutorial is a `Journal` class: we can create journals to which we `add()` entries; at some point we want to save them. It might seem natural to write `save()` method. However, we might have many similar classes that need to be saved similarly: `Notebook`, `Workbook`, etc. Thus, we centralize the saving functionality to a specific class that is concerned with the saving of many different classes; that class is called the `PersistenceManager`. Similarly, we could have a `LoadingManager` class which takes care of loading.

Advantages:

- `Journal` focuses only on adding and storing entries in memory.
- If we decide to change the saving to be in a data base instead of in a TXT, we might want to do it for all similar classes, so having everything in a centralized place is very helpful: we don't need to change the separate classes, but just the `PersistenceManager`!

```c++
struct PersistenceManager
{
  // static method: can be called even without PM is not instantiated
  // example: PersistenceManager::save(journal, "diary.txt")
  static void save(const Journal& j, const string& filename)
  {
    ofstream ofs(filename);
    for (auto& s : j.entries)
      ofs << s << endl;
  }

  // Other save() functions of similar classes would go here, too

};
```

Other concepts that appear in the code:

- `static` class members & methods
- `explicit`
- `boost::lexical_cast`

Links:

- [Single Responsibility Principle](https://en.wikipedia.org/wiki/Single-responsibility_principle)
- [Separation of Concerns](https://en.wikipedia.org/wiki/Separation_of_concerns)
- [Static Members of a C++ Class](https://www.tutorialspoint.com/cplusplus/cpp_static_members.htm)
- [Static functions outside classes](https://stackoverflow.com/questions/25724787/static-functions-outside-classes)

### Python Implementation

See the notebook [SOLID_Principles.ipynb](./01_SOLID/).

```python
class Journal:
    def __init__(self):
        self.entries = []
        self.count = 0

    def add_entry(self, text):
        self.entries.append(f"{self.count}: {text}")
        self.count += 1

    def remove_entry(self, pos):
        del self.entries[pos]

    def __str__(self):
        return "\n".join(self.entries)

    # Break SRP = Single Responsibility Principle
    # Saving is a responsibility that should be handled
    # by a class that persists the complete family
    # of journal classes!
    # Giving too many responsibilities to single classes
    # creates the anti-pattern of a God Object:
    # a gigant class which does everything,
    # which is very difficult to maintain!
    def save(self, filename):
        file = open(filename, "w")
        file.write(str(self))
        file.close()

    def load(self, filename):
        pass

    def load_from_web(self, uri):
        pass

# Persisting of objects should be handled by a spacific class
# which takes care of all faminily of journal classes.
# That way, the saving processes are all localized
# in the same spot -> easier to maintain!
class PersistenceManager:
    # Static method: it cannot access/modify either the instance or the class
    # but it can be used from both.
    # They signal that the function is independent from the class/object,
    # i.e., some kind of utility procedure; that improves mantainability.
    @staticmethod
    def save_to_file(journal, filename):
        file = open(filename, "w")
        file.write(str(journal))
        file.close()

### __main__

j = Journal()
j.add_entry("I cried today.")
j.add_entry("I ate a bug.")
print(f"Journal entries:\n{j}\n")

p = PersistenceManager()
file = r'./journal.txt'
p.save_to_file(j, file)

# verify!
with open(file) as fh:
    print(fh.read())

```

## 2. Open-Closed Principle: `01_SOLID/OCP.cpp`

The Open-Closed Principle states that the system should be 

- open to extension (e.g., by inheritance),
- but closed to modification, e.g., we don't change older code.

That is achieved by creating template classes for everything we create and inheriting them on any new use case.

The example used is a product filter: products have two properties `color` and `size` ddefine as `enums`,  and we want to filter them depending on those values. The first version of the filter is a series of functions like `filter_by_color()` nested in a `struct`; however, the `struct` needs to be changed/extended inside every time we define a new filter.

With the OCP, we transform that to have two pure virtual classes: `Specification` and `Filter`. We inherit `Specification` for each particular property. All inherited `Specifications` will have the same checking function `is_satistifed()`. Then, a `BetterFilter` class is inherited which calls that function `is_satistifed()` of generic `Specifications`, which when used, can be any particular ones.

```c++
// --- BAD PATTERN

struct ProductFilter
{
  typedef vector<Product*> Items;

  Items by_color(Items items, const Color color)
  {
    Items result;
    for (auto& i : items)
      if (i->color == color)
        result.push_back(i);
    return result;
  }

  Items by_size(Items items, const Size size)
  {
    //...
  }
};

// --- GOOD PATTERN
// Alternative to the bad one
// using the open-close principle

template <typename T> struct Specification
{
  virtual ~Specification() = default;
  virtual bool is_satisfied(T* item) const = 0;
};

template <typename T> struct Filter
{
  virtual vector<T*> filter(vector<T*> items,
                            Specification<T>& spec) = 0;
};

struct BetterFilter : Filter<Product>
{
  vector<Product*> filter(vector<Product*> items, Specification<Product> &spec) override
  {
    vector<Product*> result;
    for (auto& p : items)
      if (spec.is_satisfied(p))
        result.push_back(p);
    return result;
  }
};

struct ColorSpecification : Specification<Product>
{
  Color color;

  ColorSpecification(Color color) : color(color) {}

  bool is_satisfied(Product *item) const override {
    return item->color == color;
  }
};

```

Other code pieces/elements:
- `override`: it means it is overriding a virtual function from a base class; it appears after the function definition.
- The class `AndSpecification` is also defined with the `operator&&`: it makes possible to handle two specifications; the `operator&&` makes possible to compact the code (see in file).

### Python Implementation

See the notebook [SOLID_Principles.ipynb](./01_SOLID/).

```python
from enum import Enum

# The Enum base class
# makes possible to have enumerations
# like in C/C++
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

# Our product
class Product:
    def __init__(self, name, color, size):
        self.name = name
        self.color = color
        self.size = size

# We use generators with yield.
# yield suspends a function’s execution
# and sends a value back to the caller,
# but retains enough state to enable the function
# to resume where it left off.
# When the function resumes, 
# it continues execution immediately after the last yield run.
# This allows its code to produce a series of values over time, 
# rather than computing them at once and sending them back like a list.
# Commonly, yield is used within a loop.
class ProductFilter:
    def filter_by_color(self, products, color):
        for p in products:
            if p.color == color:
                yield p

    def filter_by_size(self, products, size):
        for p in products:
            if p.size == size:
                yield p

    def filter_by_size_and_color(self, products, size, color):
        for p in products:
            if p.color == color and p.size == size:
                yield p
    
    # BUT, this filter violates the OCP (principle)
    # OCP = open for extension, closed for modification
    # - once a class is written, we should not modify it
    # - but we should be able to extend it
    # This violation causes here additionally
    # a "state space explosion": as we add more properties,
    # the filter compbinations explode:
    # 2 criteria -> 3 filters/methods
    # 3 criteria (e.g., +Weight) -> c s w cs sw cw csw = 7 methods


# To tolve the issue of breaking OCP,
# we use a Specification + Filter classes.
# We're going to inherit override these classes,
# 
class Specification:
    def is_satisfied(self, item):
        pass

    # We overload the & operator, which makes life easier
    # In Python, we cannot overload the and operator,
    # but we can overload the & operator with __and__
    def __and__(self, other):
        return AndSpecification(self, other)

class Filter:
    def filter(self, items, spec):
        pass

# Color specification checker
class ColorSpecification(Specification):
    def __init__(self, color):
        self.color = color

    def is_satisfied(self, item):
        return item.color == self.color

# Size specification checker
class SizeSpecification(Specification):
    def __init__(self, size):
        self.size = size

    def is_satisfied(self, item):
        return item.size == self.size

# class AndSpecification(Specification):
#     def __init__(self, spec1, spec2):
#         self.spec2 = spec2
#         self.spec1 = spec1
#
#     def is_satisfied(self, item):
#         return self.spec1.is_satisfied(item) and \
#                self.spec2.is_satisfied(item)

# This is a COMBINATOR
# We give a variable number of arguments, i.e., specifications: *args
class AndSpecification(Specification):
    def __init__(self, *args):
        self.args = args

    def is_satisfied(self, item):
        # all(iterable) returns True if all items in an iterable are true,
        # otherwise it returns False.
        # If the iterable object is empty, the all() function also returns True.
        # map(fun, iterable): fun is applied to all elements of iterable
        # and the resulting iterable is returned
        # So, for all speficications in self.args
        # their is_satisfied(item) function is called.
        return all(map(lambda spec: spec.is_satisfied(item),
                       self.args))

# We could put this implementation in the base Filter class
# but instead, we do it here, because that enables
# inheriting Filter for other kind of Filter implementations
# -- that's also the OCP!
class BetterFilter(Filter):
    def filter(self, items, spec):
        for item in items:
            if spec.is_satisfied(item):
                yield item

#### __main__

apple = Product('Apple', Color.GREEN, Size.SMALL)
tree = Product('Tree', Color.GREEN, Size.LARGE)
house = Product('House', Color.BLUE, Size.LARGE)

products = [apple, tree, house]

# BAD - Breaks OCP
pf = ProductFilter()
print('Green products (old):')
for p in pf.filter_by_color(products, Color.GREEN):
    print(f' - {p.name} is green')

# GOOD - OCP Compliant
bf = BetterFilter()

print('Green products (new):')
green = ColorSpecification(Color.GREEN)
for p in bf.filter(products, green):
    print(f' - {p.name} is green')

print('Large products:')
large = SizeSpecification(Size.LARGE)
for p in bf.filter(products, large):
    print(f' - {p.name} is large')

print('Large blue items:')
# We have 2 options:
# 1. We use AndSpecification
# 2. We use the overloaded & operator from Specification, wehich returns AndSpecification
# Both work!
# 1. AndSpecification
# large_blue = AndSpecification(large, ColorSpecification(Color.BLUE))
# 2. Overloaded &
large_blue = large & ColorSpecification(Color.BLUE)
for p in bf.filter(products, large_blue):
    print(f' - {p.name} is large and blue')

```

## 3. Liskov Substitution Principle: `01_SOLID/LSP.cpp`

Named after [Barbara Liskov](https://en.wikipedia.org/wiki/Barbara_Liskov), this principle states that **subtypes should be immediately substitutable by their base types**.

The example given uses the classes `Rectangle` and `Square`. Although it may seem sensible to inherit `Square` from `Rectangle`, the `set_width/height()` functions enter in conflict: a square changes both dimensions when one is set. Thus, we get unexpected behavior. The solution is not using inheritance and working with squares as if they were rectangles. A factory is used to create differentiated objects, but they are rectangles at the end.

```c++
class Rectangle
{
// Protexted: accessible from within the class, inherited class & children
protected:
  int width, height;
public:
  Rectangle(const int width, const int height)
    : width{width}, height{height} { }

  // set_* is virtual so that they are overridden in child class Square
  int get_width() const { return width; }
  virtual void set_width(const int width) { this->width = width; }
  int get_height() const { return height; }
  virtual void set_height(const int height) { this->height = height; }

  int area() const { return width * height; }
};

// Square is inherited from Rectangle
// It sounds plausible, but doing so, when we redefine the set_*
// methods, the Liskov substitution principle is broken!
// We cannot substitute a square by a rectangle
class Square : public Rectangle
{
public:
  Square(int size): Rectangle(size,size) {}
  // We override virtual set_* functions
  void set_width(const int width) override {
    // Setting both the height and the width with size
    // is correct for the Square, but wrong for the Rectangle.
    // We are breaking the Liskov substitution principle!
    this->width = height = width;
  }
  void set_height(const int height) override {
    this->height = width = height;
  }
};

// Possible solutions to avoid breaking Liskov:
// - Square maybe should not be inherited from Rectangle
// - Instead, we could use Rectangle, and (1) add a flag inside to denote when it's a square
// - or, (2) we can use a factory with Rectangles.
// The factory creates rectangles or squares, but it always returns Rectangles.
struct RectangleFactory
{
  // Static functions: they can be called without instantiating RectangleFactory
  // Functions to be implemented.
  static Rectangle create_rectangle(int w, int h);
  static Rectangle create_square(int size);
};

// This function processes Rectangles passed by reference
// so we can pass also Squares.
// BUT: Since the Liskov substitution principe is broken,
// it won't work as expected.
void process(Rectangle& r)
{
  int w = r.get_width();
  r.set_height(10);

  std::cout << "expected area = " << (w * 10) 
    << ", got " << r.area() << std::endl;
}

int main()
{
  Rectangle r{ 5,5 };
  process(r);

  Square s{ 5 };
  process(s);

  //getchar();
  return 0;
}
```

### Python Implementation

```python
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

### __main__

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

```

## 4. Interface Segregation Principle: `01_SOLID/ISP.cpp`

The idea is to avoid interfaces which are too large.

An example is given with a multi-function printer that is able to print and scan.  
Instead of implementing a complex interface which provides with the `print()` and `scan()` functions, we break it down to two interfaces that are later used in a third interface.

```c++

// --- BAD PATTERN

struct IMachine
{
  virtual void print(Document& doc) = 0;
  virtual void fax(Document& doc) = 0;
  virtual void scan(Document& doc) = 0;
};

struct MFP : IMachine
{
  void print(Document& doc) override;
  void fax(Document& doc) override;
  void scan(Document& doc) override;
};

// --- GOOD PATTERN

// Abstract, Interface
struct IPrinter
{
  virtual void print(Document& doc) = 0;
};

// Abstract, Interface
struct IScanner
{
  virtual void scan(Document& doc) = 0;
};

// Concrete class
struct Printer : IPrinter
{
  void print(Document& doc) override;
};

// Concrete class
struct Scanner : IScanner
{
  void scan(Document& doc) override;
};

// Abstract, Interface
struct IMachine: IPrinter, IScanner
{
};

// Concrete class
struct Machine : IMachine
{
  IPrinter& printer;
  IScanner& scanner;

  Machine(IPrinter& printer, IScanner& scanner)
    : printer{printer},
      scanner{scanner}
  {
  }

  void print(Document& doc) override {
    printer.print(doc);
  }
  void scan(Document& doc) override;
};

```

### Python Implementation

```python
from abc import abstractmethod

class Machine:
    def print(self, document):
        raise NotImplementedError

    def fax(self, document):
        raise NotImplementedError

    def scan(self, document):
        raise NotImplementedError

# A multi-function device works with all the
# interfaces from Machine, so it's OK
class MultiFunctionPrinter(Machine):
    def print(self, document):
        pass # we would write our implementation

    def fax(self, document):
        pass # we would write our implementation

    def scan(self, document):
        pass # we would write our implementation

# An old-fashioned printer is not expected to have all the
# functionalities in Machine!
class OldFashionedPrinter(Machine):
    def print(self, document):
        # OK for an old-fashioned printer, it can print
        pass # we would write our implementation

    def fax(self, document):
        # No operation: an old-fashioned printer cannot fax!
        pass  # do-nothing: problematic, because the interface is there!

    # An old-fashioned printer cannot scan
    def scan(self, document):
        """Not supported!"""
        # Another option to doing nothing is raising an error
        # but it crashes the code.
        raise NotImplementedError('Printer cannot scan!')

## Solution: we create classes for each functionality and then combine them!

# Abstract class: not to be instantiate, only inherited
class Printer:
    # Abstract method: not implemented
    @abstractmethod
    def print(self, document): pass

class Scanner:
    @abstractmethod
    def scan(self, document): pass

class FaxMachine:
    @abstractmethod
    def fax(self, document): pass

# Concrete classes inheriting base abstract classes
class MyPrinter(Printer):
    def print(self, document):
        print(document)

class Photocopier(Printer, Scanner):
    def print(self, document):
        print(document)

    def scan(self, document):
        pass  # something meaningful

# Abstract class which combines several abstract classes
class MultiFunctionDevice(Printer, Scanner, FaxMachine):
    @abstractmethod
    def print(self, document):
        pass

    @abstractmethod
    def scan(self, document):
        pass

    @abstractmethod
    def fax(self, document):
        pass
    
class MultiFunctionMachine(MultiFunctionDevice):
    #def __init__(self, printer, scanner, faxmachine):
    #    self.printer = printer
    #    self.scanner = scanner
    #    self.faxmachine = faxmachine

    def print(self, document):
        #self.printer.print(document)
        print("printing", document)
        
    def scan(self, document):
        #self.scanner.scan(document)
        print("scanning", document)
        
    def fax(self, document):
        #self.faxmachine.fax(document)
        print("faxing", document)
        
### __main__

my_machine = MultiFunctionMachine()
my_machine.print('test')
my_machine.fax('test')
my_machine.scan('test')

# This will raise an error
printer = OldFashionedPrinter()
printer.fax(123)  # nothing happens
printer.scan(123)  # oops!

```

## 5. Dependency Inversion Principle: `01_SOLID/DIP.cpp`

The Dependency Inversion Principle is based on the following two concepts:

1. High-level modules should not depend on low-level modules. Both should depend on abstractions.
2. Abstractions should not depend on details. Details should depend on abstractions.

It is a way of protecting from implementation changes in low-level modules. Note that:

- low-level modules/classes are the ones which deal with storage, or similar,
- high-level modules/classes are the ones which deal with browsing stored objects, or similar.

Don't confuse it with the *dependency injection*, it doesn't directly relate to it.

Example in python: a constellation of classes which deals with:

- Persons
- Relationships between them (parent, child, etc.)
- And a browsing class which researches from stored relationships

```python
from abc import abstractmethod
from enum import Enum


class Relationship(Enum):
    PARENT = 0
    CHILD = 1
    SIBLING = 2


class Person:
    def __init__(self, name):
        self.name = name


class RelationshipBrowser:
    @abstractmethod
    def find_all_children_of(self, name): pass


class Relationships(RelationshipBrowser):  # low-level
    def __init__(self):
        self.relations = []

    def add_parent_and_child(self, parent, child):
        self.relations.append((parent, Relationship.PARENT, child))
        self.relations.append((child, Relationship.CHILD, parent))
            
    def find_all_children_of(self, name):
        for r in self.relations:
            if r[0].name == name and r[1] == Relationship.PARENT:
                yield r[2].name

# We could have used the relations list from Relationships
# but that's risky: if we change the storage implementation of the relations
# this high-level class breaks. Thus, instead, we create and use interfaces:
# - a RelationshipBrowser interface is created, used to inherit Relationships
# - the browser has abstract methods which find relations in which occur names
# - the high level class uses the browser to find relations, so no low-level strucures are used directly!
# Therefore, changing low-level classes doesn't affect high-level ones!
class Research: # high-level
    # dependency on a low-level module directly
    # bad because strongly dependent on e.g. storage type

    # def __init__(self, relationships):
    #     # high-level: find all of john's children
    #     relations = relationships.relations
    #     for r in relations:
    #         if r[0].name == 'John' and r[1] == Relationship.PARENT:
    #             print(f'John has a child called {r[2].name}.')

    def __init__(self, browser):
        for p in browser.find_all_children_of("John"):
            print(f'John has a child called {p}')

### __main__
            
parent = Person('John')
child1 = Person('Chris')
child2 = Person('Matt')

# low-level module
relationships = Relationships()
relationships.add_parent_and_child(parent, child1)
relationships.add_parent_and_child(parent, child2)

Research(relationships)
```