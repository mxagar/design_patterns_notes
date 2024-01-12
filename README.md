# Notes on Design Patterns (C++ and Python)

This guide and its related files were created while following the Udemy courses

- [Design Patterns in Modern C++](https://www.udemy.com/course/patterns-cplusplus/)
- [Design Patterns in Python](https://www.udemy.com/course/design-patterns-python/)

by Dmitri Nesteruk.

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

## What Are Design Patterns?

Design Patterns are common and re-usable programming approaches that were popularized in the book of the same name (by "the gang of four": Gamma, Helm, Johnson & Vlissides).
They have been internalized to some languages and every programmer should know them, since they are the basic vocabulary and grammar for software architecture.

According to the Gamma categorization (Erich Gamma, from the Gang of Four), there are three types of patterns:

1. Creational
2. Structural
3. Behavioral

This guide compiles all the patterns defined in the book by the Gang of Four and additionally introduces the SOLID principles:

1. SOLID Design Principles
   - Single Responsibility
   - Open-Closed
   - Liskov Substitution
   - Interface Segregation
   - Dependency Inversion
2. Creational Patterns
   - Builder
   - Factories: Abstract, Factory Method
   - Prototype
   - Singleton
3. Structural Patterns
   - Adapter
   - Bridge
   - Composite
   - Decorator
   - Facade
   - Flyweight
   - Proxy
4. Behavioral Patterns
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

I use both Python and C++ in the notes and code examples.

### C++

The [boost](https://www.boost.org/) libraries are used throughout the course. To install it on a Mac:

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

## Authorship

Original code and examples: Dmitri Nesteruk.

Code modifications and note: Mikel Sagardia, 2022.  
No guaranties.
