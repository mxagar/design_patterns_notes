# Design Patterns

This guide and its related files were created while following the Udemy course

[Design Patterns in Modern C++](https://www.udemy.com/course/patterns-cplusplus/)

by Dmitri Nesteruk, and the following popular books:

- "Design Patterns" (Addison Wesley), by Gamma, Helm, Johnson & Vlissides
- "Design Patterns" (O'Reailly Head First), by Kathy Sierra and Bert Bates

The file `DesignPatterns_Guide.md` contains all the notes I made; look in the co-located folders for specific pattern material.

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

SOLID Design Principles were introduced by Robert C. Martin (Uncle Bob), known also for the Agile Manifesto.

