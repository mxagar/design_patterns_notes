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

Different examples are provided: an HTML builder, a Car builder and a Person builder. In general:

- We have an Object class and a Builder class which builds those objects.
- The Builder has methods that added components to the Object.
- We can either explicitly use the Builder or return it from the Object using a `create()` static method.
- We can make the builder fluent so that the methods that add components are chained.
- Different facets of an Object can be built with different Builder classes that work in tandem.

In the following, only the Car example is provided; check the notebook for more.

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

## 2. Factories

## 3. Prototype

## 4. Singleton

