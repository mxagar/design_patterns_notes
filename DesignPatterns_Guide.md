# Design Patterns

This guide and its related files were created while following the Udemy course

[Design Patterns in Modern C++](https://www.udemy.com/course/patterns-cplusplus/)

by Dmitri Nesteruk, and the following popular books:

- "Design Patterns" (Addison Wesley), by Gamma, Helm, Johnson & Vlissides
- "Design Patterns" (O'Reailly Head First), by Kathy Sierra and Bert Bates

The file `DesignPatterns_Guide.md` contains all the notes I made; look in the co-located folders for specific pattern code.

I found a repository by Dmitri Nesteruk, which I forked

- [https://github.com/mxagar/DesignPatternsWebinar](https://github.com/mxagar/DesignPatternsWebinar)
- [https://github.com/nesteruk/DesignPatternsWebinar](https://github.com/nesteruk/DesignPatternsWebinar)

However, the current repository builds up on that one and re-structures the complete code. However, note that the original example code is by Dmitri Nesteruk.

Mikel Sagardia, 2022.
No warranties.

Overview of sections:

1. Introduction: SOLID Design Principles
2. Builder (Pattern)

## 1. Introduction: SOLID Design Principles

Design Patterns are common and re-usable programming approaches that were popularized in the book of the same name (by "the gang of four": Gamma, Helm, Johnson & Vlissides).
They have been internalized to some languages and every programmer should know them, since they are the basic vocabulary and grammar for software architecture.

Structucture of contents:
- SOLID Design Principles
- Creational Patterns
  - Builder
  - Factories: Absract, Factory Method
  - Prototype
  - Singleton
- Structural Patterns
  - Adapter
  - Bridge
  - Composite
  - Decorator
  - Facade
  - Flyweight
  - Proxy
- Behavioral Patterns
  - Chain of Responsibility
  - Commandd
  - Interpreter
  - Iterator
  - Mediator
  - Memento
  - Observer
  - State
  - Strategy
  - Template Method
  - Visitor

The instructor warns that, for the sake of simplicity, there are some simplifications in his examples: liberal use of public members, lack of virtual destructors, passing/returning by value, lack of move operations...

The [boost]() library is used throughout the course. To install it on a mac:

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

### SOLID Design Principles

SOLID Design Principles were introduced by Robert C. Martin (Uncle Bob), known also for the Agile Manifesto:

1. S: Single Responsibility Principle

### 1. Single Responsibility Principle: `01_Intro/SRP.cpp`

A class should take one responsibility, and only one. That way, we are going to have only one reason to change it. That is related to the **separation of concerns**: we assign clear concerns to specific classes.

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

### 1. Open-Closed Principle: `01_Intro/SRP.cpp`
