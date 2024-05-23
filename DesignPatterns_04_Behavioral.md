# Design Patterns: Behavioral Patterns

This document/guide is the fourth from a set of 4 documents:

1. SOLID Design Principles
2. Creational Patterns
3. Structural Patterns
4. **Behavioral Patterns**

See the overview file [`README.md`](README.md) for more information on the origin of the guides.

In the present guide, the **Behavioral Patterns** are defined and examples are given.

Behavioral patterns don't really follow any central theme:

- They are all different.
- Sometimes they overlap in their function, i.e., the goal they achieve, but the underlying mechanisms are different.

Table of Contents:

- [Design Patterns: Behavioral Patterns](#design-patterns-behavioral-patterns)
  - [1. Chain of Responsibility](#1-chain-of-responsibility)

## 1. Chain of Responsibility

Software components are often built with hierarchical relationships. Those relationships can capture resposibility, similarly as it can happen in a company (CEO, manager, employee). The pattern Chain of Responsibility is a chain of components in which all get a change to process a command or a query, optionally having a default processing implementation and an ability to terminate the processing chain.

In other words, Chain of Responsibility allows an object to pass a request along a chain of potential handlers until the request is handled. This pattern decouples the sender of the request from the receiver by giving multiple objects a chance to handle the request.
 
For example:

- In a GUI, we click a graphical element on a form
  - The button handles the action, which leads to stopping the processing
  - Or the underlying group box can handle it
  - Or the underlying window can handle it
- A card computer game
  - A creature has attack and defense skills
  - Thos skills can be boosted by other card creatures
- Support
  - We can have first-level or basic support
  - Or second-level = advanced support
  - Or third-level = expert support

Some key components that often appear in Chain of Responsibility are:

- **Handler**: Defines an interface for handling requests and for setting the next handler in the chain.
- **ConcreteHandler**: Implements the Handler interface and processes requests it is responsible for. If it can't handle the request, it forwards the request to the next handler in the chain.
- **Client**: Initiates the request and passes it to the first handler in the chain.

Notebook: [`Behavioral_Patterns.ipynb`](./04_Behavioral_Patterns/Behavioral_Patterns.ipynb)

In the notebook, three examples are shown to illustrate the abovementioned 3 concepts:

- **Support**: example shown below
- Game Card; see the notebook.
- Game Card with Broker and Queries; see the notebook.

In the last example, the **Command and Query Separation (CQS)** principle is used: Whenever we operate on objects, we separate all the invokations into two types:

- Command: invokation which asks for an action or a change; e.g., set value to X.
- Query: ask/retrieve information without changing anything, e.g., get value of X.

Separating both Commands and Queries is known as the Command and Query Separation (CQS) Principle. It is a design priciple with some benefits:

- Clarity: Separating commands and queries makes it clear which methods are performing actions and which are retrieving information.
- Simpler Testing: Queries are easier to test because they are idempotent and do not change the state.
- Improved Maintainability: Clear separation of responsibilities makes the code easier to understand and maintain.

Support example:

```python
# Abstract Handler:
# Defines an interface for handling requests 
# and for setting the next handler in the chain.
# SupportHandler will be inherited by concrete handlers!
class SupportHandler:
    def __init__(self):
        # The next_handler is a pointer to the next handler
        # which is set with set_next_handler
        # when setting the Chain of Responsibility
        self.next_handler = None

    # This method is used to set the
    # Chain of Responsibility
    def set_next_handler(self, handler):
        self.next_handler = handler

    # This handle_request method is called by the concrete
    # class/object if the type of issue to handle 
    # does not belong to the type of the concrete handler
    def handle_request(self, issue):
        if self.next_handler:
            return self.next_handler.handle_request(issue)
        else:
            return "No handler available for this issue"

# Concrete Handlers:
# They implement the Handler interface 
# and processes requests it is responsible for. 
# If they can't handle the request, 
# they forward the request to the next handler in the chain.
class BasicSupport(SupportHandler):
    def handle_request(self, issue):
        if issue == "basic":
            return "BasicSupport: Handling basic issue"
        else:
            # We call the abstract handler
            # which calls the next handler
            # in the Chain of Responsibility
            return super().handle_request(issue)

class AdvancedSupport(SupportHandler):
    def handle_request(self, issue):
        if issue == "advanced":
            return "AdvancedSupport: Handling advanced issue"
        else:
            return super().handle_request(issue)

class ExpertSupport(SupportHandler):
    def handle_request(self, issue):
        if issue == "expert":
            return "ExpertSupport: Handling expert issue"
        else:
            return super().handle_request(issue)

# __main__: Client
# Initiates the request and passes it 
# to the first handler in the chain.

# Create handlers
basic = BasicSupport()
advanced = AdvancedSupport()
expert = ExpertSupport()

# Set up Chain of Responsibility
# Basic -> Advanced -> Expert
basic.set_next_handler(advanced)
advanced.set_next_handler(expert)

# Client issues
# In this simple example, 
# each issue is a string that specifies the type of issue,
# i.e., we use it to decide which handler should process it
issues = ["basic", "advanced", "expert", "unknown"]

for issue in issues:
    print(f"Issue: {issue} - Response: {basic.handle_request(issue)}")
# Issue: basic - Response: BasicSupport: Handling basic issue
# Issue: advanced - Response: AdvancedSupport: Handling advanced issue
# Issue: expert - Response: ExpertSupport: Handling expert issue
# Issue: unknown - Response: No handler available for this issue
```

