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
    - [Python](#python)
  - [2. Open-Closed Principle: `01_SOLID/OCP.cpp`](#2-open-closed-principle-01_solidocpcpp)
  - [3. Liskov Substitution Principle: `01_SOLID/LSP.cpp`](#3-liskov-substitution-principle-01_solidlspcpp)
  - [4. Interface Segregation Principle: `01_SOLID/ISP.cpp`](#4-interface-segregation-principle-01_solidispcpp)
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

### Python

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
- but closed to modification, e.g., we don' change older code.

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

## 3. Liskov Substitution Principle: `01_SOLID/LSP.cpp`

Named after [Barbara Liskov](https://en.wikipedia.org/wiki/Barbara_Liskov), this principle states that **subtypes should be immediately substitutable by their base types**.

The example given uses the classes `Rectangle` and `Square`. Although it may seem sensible to inherit `Square` from `Rectangle`, the `set_width/height()` functions enter in conflict: a square changes both dimensions when one is set. Thus, we get inexpected behavior. The solution is not using inheritance and working with squares as if they were rectangles. A factory is used to create differentiated objects, but they are rectangles at the end.

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

## 4. Interface Segregation Principle: `01_SOLID/ISP.cpp`

The idea is to avoid interfaces which are too large.

An example is given with a multi-function printer that is able to print and scan.  
Instead of implementing a complex interface which provides with the `print()` and `scan()` functions, we break it down to two interfaces that are later used in a thirds interface.

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

## 5. Dependency Inversion Principle: `01_SOLID/DIP.cpp`

The Dependency Inversion Principle is based on the following two concepts:

1. High-level modules should not depend on low-level modules. Both should depend on abstractions.
2. Abstractions should not depend on details. Details should depend on abstractions.

It is a way of protecting from implementation changes in low-level modules.