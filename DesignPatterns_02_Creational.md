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






## 2. Factories

## 3. Prototype

## 4. Singleton

