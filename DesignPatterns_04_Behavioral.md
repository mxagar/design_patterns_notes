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
  - [Command](#command)
  - [Interpreter](#interpreter)
    - [Lexing](#lexing)
    - [Parsing](#parsing)
  - [Iterator](#iterator)
  - [Mediator](#mediator)
  - [Memento](#memento)
    - [Example: Bank Account](#example-bank-account)
    - [Example: Bank Account with Undo and Redo](#example-bank-account-with-undo-and-redo)
  - [Observer](#observer)
    - [Events](#events)
    - [Property Observers](#property-observers)
    - [Property Dependencies](#property-dependencies)
  - [State (Machine)](#state-machine)
    - [Handmade State Machine](#handmade-state-machine)
    - [Switch-Based State Machine](#switch-based-state-machine)
  - [Strategy](#strategy)
    - [Example: Text Processor](#example-text-processor)
  - [Template Method](#template-method)
    - [Example: Chess Game](#example-chess-game)

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

## Command

A Command is an object which represents an instruction to perform a particular action; it contains all the information necessary for the action to be taken.

- Ordinary statements are perishable:
  - They cannot undo member assignment:
  - They cannot directly serialize a sequence of actions (calls).
- We want an object that represents an operation.
  - Example: `person` should change its `age` to value `22`; the operation not only happens, but it is recoded it happened, along with who ordered it.
  - Example: `car` should `start()`.
- There are many uses for Commands: GUI commands, multi-level undo/redo, macro recording, and more!

Notebook: [`Behavioral_Patterns.ipynb`](./04_Behavioral_Patterns/Behavioral_Patterns.ipynb).

There are two examples in the notebook:

- A Command applied to a bank account.
- The same example, but with Composite Command, aka. Macro.

Bank account example:

```python
from abc import ABC, abstractmethod
from enum import Enum

# Bank account class
# This class works nicely
# but we'd like to add the undo option
# for the opreations described in it.
# We can do that with a ledger/record.
# We can do that with a Command, too.
class BankAccount:
    OVERDRAFT_LIMIT = -500

    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f'Deposited {amount}, balance = {self.balance}')

    def withdraw(self, amount):
        if self.balance - amount >= BankAccount.OVERDRAFT_LIMIT:
            self.balance -= amount
            print(f'Withdrew {amount}, balance = {self.balance}')
            # We need to return if it succeeded to avoid illegal operations
            return True
        return False

    def __str__(self):
        return f'Balance = {self.balance}'


# Optional, not necessary, but good pratice
class Command(ABC):
    # We could also use __call__, but invoke is more explicit
    @abstractmethod
    def invoke(self):
        pass

    @abstractmethod
    def undo(self):
        pass


# This Command class is a wrapper for the BankAccount
# which adds the Command functionality.
# The action on the BankAccount is not performed instantaneously
# but when we invoke() it.
# Additionally, we can undo the action.
class BankAccountCommand(Command):
    def __init__(self, account, action, amount):
        self.amount = amount
        self.action = action
        self.account = account
        self.success = None

    class Action(Enum):
        DEPOSIT = 0
        WITHDRAW = 1

    def invoke(self):
        if self.action == self.Action.DEPOSIT:
            self.account.deposit(self.amount)
            self.success = True
        elif self.action == self.Action.WITHDRAW:
            self.success = self.account.withdraw(self.amount)

    def undo(self):
        # To avoid illegal operations:
        # if the operation wasn't successful, don't allow undo
        if not self.success:
            return
        # Strictly speaking this is not correct
        # (you don't undo a deposit by withdrawing)
        # but it works for this demo, so...
        if self.action == self.Action.DEPOSIT:
            self.account.withdraw(self.amount)
        elif self.action == self.Action.WITHDRAW:
            self.account.deposit(self.amount)

# __main__
ba = BankAccount()
cmd = BankAccountCommand(ba, BankAccountCommand.Action.DEPOSIT, 100)
cmd.invoke()
print('After $100 deposit:', ba)

cmd.undo()
print('$100 deposit undone:', ba)

illegal_cmd = BankAccountCommand(ba, BankAccountCommand.Action.WITHDRAW, 1000)
illegal_cmd.invoke()
print('After impossible withdrawal:', ba)
illegal_cmd.undo()
print('After undo:', ba)
# Deposited 100, balance = 100
# After $100 deposit: Balance = 100
# Withdrew 100, balance = 0
# $100 deposit undone: Balance = 0
# After impossible withdrawal: Balance = 0
# After undo: Balance = 0
```

## Interpreter

The Interpreter is related to the processing that text requires to interpret what to do with it:

- Textual input needs to be processed; e.g., code turned in to OOP structures (compilers).
- Some examples:
  - Programming language compilers, interpreters and IDEs.
  - HTML, XML, and similar
  - Numeric expressions (`3 + 4/5`)
  - Regular expressions

Often, the processing is done to obtain structured meaning. To that end:

- We separate it into lexical tokens (*lexing*)
- and then interpret the resulting sequences (*parsing*).

Notebook: [`Behavioral_Patterns.ipynb`](./04_Behavioral_Patterns/Behavioral_Patterns.ipynb).

In the provided example numeric expressions with `+` and `-` operations are processed with an interpreter.

### Lexing

In this section, we separate the input string into a sequence of known tokens. That's called *lexing*.

```python
from enum import Enum, auto


class Token:
    # Class-level enum
    class Type(Enum):
        INTEGER = auto()
        PLUS = auto()
        MINUS = auto()
        LPAREN = auto() # (
        RPAREN = auto() # )

    def __init__(self, type, text):
        self.type = type
        self.text = text

    def __str__(self):
        return f'`{self.text}`'


# Lexing
def lex(input):
    result = []

    i = 0
    while i < len(input):
        if input[i] == '+':
            result.append(Token(Token.Type.PLUS, '+'))
        elif input[i] == '-':
            result.append(Token(Token.Type.MINUS, '-'))
        elif input[i] == '(':
            result.append(Token(Token.Type.LPAREN, '('))
        elif input[i] == ')':
            result.append(Token(Token.Type.RPAREN, ')'))
        else:  # must be a number
            digits = [input[i]]
            for j in range(i + 1, len(input)):
                if input[j].isdigit():
                    digits.append(input[j])
                    i += 1
                else:
                    result.append(Token(Token.Type.INTEGER,
                                        ''.join(digits)))
                    break
        i += 1

    return result
```

### Parsing

In this section, we take the sequence of tokens and interpret their meaning, aka. *parsing*.

```python
class Integer:
    def __init__(self, value):
        self.value = value


class BinaryOperation:
    class Type(Enum):
        ADDITION = 0
        SUBTRACTION = 1

    def __init__(self):
        self.type = None
        self.left = None
        self.right = None

    @property
    def value(self):
        if self.type == self.Type.ADDITION:
            return self.left.value + self.right.value
        elif self.type == self.Type.SUBTRACTION:
            return self.left.value - self.right.value


def parse(tokens):
    result = BinaryOperation()
    have_lhs = False # left-hand-side
    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token.type == Token.Type.INTEGER:
            integer = Integer(int(token.text))
            if not have_lhs:
                result.left = integer
                have_lhs = True
            else:
                result.right = integer
        elif token.type == Token.Type.PLUS:
            result.type = BinaryOperation.Type.ADDITION
        elif token.type == Token.Type.MINUS:
            result.type = BinaryOperation.Type.SUBTRACTION
        elif token.type == Token.Type.LPAREN:  # note: no if for RPAREN
            j = i
            while j < len(tokens):
                if tokens[j].type == Token.Type.RPAREN:
                    break
                j += 1
            # preprocess subexpression
            subexpression = tokens[i + 1:j]
            element = parse(subexpression)
            if not have_lhs:
                result.left = element
                have_lhs = True
            else:
                result.right = element
            i = j  # advance
        i += 1
    return result

def eval(input):
    tokens = lex(input)
    print(' '.join(map(str, tokens)))

    parsed = parse(tokens)
    print(f'{input} = {parsed.value}')

# __main__
eval('(13+4)-(12+1)')
eval('1+(3-4)')

# this won't work
eval('1+2+(3-4)')
```

## Iterator

- Iteration (traversal) is a core functionality of various data structures; note that some data structures (like trees) don't have a straightforward iteration process.
- An iterator is a class that facilitates the traversal
  - Keeps a reference to the current element.
  - Knows how to move to a different element.
- The iterator protocol requires:
  - `__iter__()` to expose the iterator, which uses
  - `__next__()` to return each of the iterated elements or
  - `raise StopIteration` when it's done.
- In Python, we have the keyword `token` which makes iteration very easy.

Notebook: [`Behavioral_Patterns.ipynb`](./04_Behavioral_Patterns/Behavioral_Patterns.ipynb).

The example in the notebook shows the Iterator of a Binary Tree:

```python
class Node:
    def __init__(self, value, left=None, right=None):
        self.right = right
        self.left = left
        self.value = value

        self.parent = None

        if left:
            self.left.parent = self
        if right:
            self.right.parent = self

    # We expose the tree/Node with __iter__
    def __iter__(self):
        # We use the Iterator we want here
        return InOrderIterator(self)

# Recall we can perform 3 traversals in a tree
#       1
#     /   \
#    2     3
# in-order: 2-1-3 (we implement only this one)
# pre-order: 1-2-3
# post-order: 2-3-1
class InOrderIterator:
    def __init__(self, root):
        self.root = self.current = root
        self.yielded_start = False
        while self.current.left:
            self.current = self.current.left

    # This is a tricky implementation of in-order
    def __next__(self):
        if not self.yielded_start:
            self.yielded_start = True
            return self.current

        if self.current.right:
            self.current = self.current.right
            while self.current.left:
                self.current = self.current.left
            return self.current
        else:
            p = self.current.parent
            while p and self.current == p.right:
                self.current = p
                p = p.parent
            self.current = p
            if self.current:
                return self.current
            else:
              raise StopIteration

def traverse_in_order(root):
    # This is the usual implementation of in-order
    # It leverages the use of yield
    def traverse(current):
        if current.left:
            for left in traverse(current.left):
                yield left
        yield current
        if current.right:
            for right in traverse(current.right):
                yield right
    for node in traverse(root):
        yield node


# __main__

# Recall we can perform 3 traversals in a tree
#       1
#     /   \
#    2     3
# in-order: 2-1-3 (we implement only this one)
# pre-order: 1-2-3
# post-order: 2-3-1
root = Node(1,
            Node(2),
            Node(3))

# We can iterate with iter and next
it = iter(root)
print([next(it).value for x in range(3)])

# Or, since we have __iter__, in a loop
for x in root:
    print(x.value)

for y in traverse_in_order(root):
    print(y.value)
```

## Mediator

The Mediator facilitates communication between different components without them necessarily being aware of each other or having direct (reference) access to each other.

- Components may go in and out of a system at any time. For instance:
  - Chatroom participants
  - Players in an online game
- It makes no sense for rthem to have direct reference to one another
  - Because those references may go dead
- Solution: we can have them all refer to some central component that facilitates communication, i.e., the Mediator.
  - All components in the system refer to the Mediator.
  - The Mediator engages in bidirectional communication with its connected components.
  - The Mediator has functions that the components can call.
  - The components have functions that the Mediator can call.
  - We can also work with events.

Notebook: [`Behavioral_Patterns.ipynb`](./04_Behavioral_Patterns/Behavioral_Patterns.ipynb).

Two examples ae shown in the notebook:

- A chatroom (summarized here).
- A game with events.

```python
class Person:
    def __init__(self, name):
        self.name = name
        self.chat_log = []
        self.room = None

    def receive(self, sender, message):
        s = f'{sender}: {message}'
        print(f'[{self.name}\'s chat session] {s}')
        self.chat_log.append(s)

    def say(self, message):
        self.room.broadcast(self.name, message)

    def private_message(self, who, message):
        self.room.message(self.name, who, message)

# This is our Mediator,
# since it allows private and broadcasting messages
class ChatRoom:
    def __init__(self):
        self.people = []

    # Broadcast = message to all
    # We should send a message to everybody
    # except the source
    # We traverse all users and make them receive()
    # the message
    def broadcast(self, source, message):
        for p in self.people:
            if p.name != source:
                p.receive(source, message)

    def join(self, person):
        join_msg = f'{person.name} joins the chat'
        self.broadcast('room', join_msg)
        person.room = self
        self.people.append(person)

    # Message = message to one specififc person
    # We traverse all users and make _only_
    # the specific user receive()
    # the message
    def message(self, source, destination, message):
        for p in self.people:
            if p.name == destination:
                p.receive(source, message)

# __main__
room = ChatRoom()

john = Person('John')
jane = Person('Jane')

room.join(john)
room.join(jane)

john.say('hi room')
jane.say('oh, hey john')

simon = Person('Simon')
room.join(simon)
simon.say('hi everyone!')

jane.private_message('Simon', 'glad you could join us!')

# [John's chat session] room: Jane joins the chat
# [Jane's chat session] John: hi room
# [John's chat session] Jane: oh, hey john
# [John's chat session] room: Simon joins the chat
# [Jane's chat session] room: Simon joins the chat
# [John's chat session] Simon: hi everyone!
# [Jane's chat session] Simon: hi everyone!
# [Simon's chat session] Jane: glad you could join us!
```

## Memento

- An object or a system can go through several changes.
  - Example: a bank account gets deposits and withdrawals.
- There are different ways of navigating those changes.
  - One way is to record every change (Command) and teach a command to *undo* itself.
  - Another is to simply save snapshots of the system = Memento.
- The Memento pattern is a token/handle class representing the system state.
  - It lets us roll back to the state when the token was generated.
  - It may or may not expose state information.

So, basically, the Memento pattern is like a history, i.e., a list of all states along the time. Whenever we perform a change, a state is saved so that we can go back/forth in the history of object states.

### Example: Bank Account

In this example, for every deposit we do in a bank account, a Memento (state = balance) object is returned. Given a Memento of a bank account, we can restore that bank account with the state of the Memento.

```python
# We could call it BanckAccountSnapshot
# In this simple example, the state is just the balance
class Memento:
    def __init__(self, balance):
        self.balance = balance


class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return Memento(self.balance)

    def restore(self, memento):
        self.balance = memento.balance

    def __str__(self):
        return f'Balance = {self.balance}'

# __main__
ba = BankAccount(100)
m1 = ba.deposit(50)
m2 = ba.deposit(25)
print(ba)

# restore to m1
ba.restore(m1)
print(ba)

# restore to m2
ba.restore(m2)
print(ba)
# Balance = 175
# Balance = 150
# Balance = 175
```

### Example: Bank Account with Undo and Redo

This example builds on the previous one. We build a list of all the changes (a list of Mementos) in the bank account.

```python
class Memento:
    def __init__(self, balance):
        self.balance = balance


class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
        self.changes = [Memento(self.balance)] # our history
        self.current = 0 # index where we are in changes

    def deposit(self, amount):
        self.balance += amount
        m = Memento(self.balance)
        self.changes.append(m)
        self.current += 1
        return m

    def restore(self, memento):
        if memento:
            self.balance = memento.balance
            self.changes.append(memento)
            self.current = len(self.changes)-1

    def undo(self):
        # We go back one step in history/changes
        if self.current > 0:
            self.current -= 1
            m = self.changes[self.current]
            self.balance = m.balance
            return m
        return None

    def redo(self):
        # We go one step forward in history/changes
        if self.current + 1 < len(self.changes):
            self.current += 1
            m = self.changes[self.current]
            self.balance = m.balance
            return m
        return None

    def __str__(self):
        return f'Balance = {self.balance}'

# __main__
ba = BankAccount(100)
ba.deposit(50)
ba.deposit(25)
print(ba)

ba.undo()
print(f'Undo 1: {ba}')
ba.undo()
print(f'Undo 2: {ba}')
ba.redo()
print(f'Redo 1: {ba}')
# Balance = 175
# Undo 1: Balance = 150
# Undo 2: Balance = 100
# Redo 1: Balance = 150
```

## Observer

The Observer is probably the most common pattern.

- We need to be informed when certain things happen
  - Object's property changes
  - Object does something
  - Some external event occurs
- We want to listen to those events and we want to be notified when they occur
  - Notifications should include useful data
- We want to unsubscribe from events we're no longer interested in

The Observer is an object that wishes to be informed about events happening in the system. The entity generating the events is an *observable*.

One common use-case is when a class property changes; we can use Python `@property.setter` decorator to invoke callable `Event` objects, which consist of lists of functions which are run when an event occurs.

Also, note that:

- In general, the Observer is an intrusive approach, i.e., the observable must provide an event to subscribe to.
- Subscription and unsubscription is handled with addition/removal of items in a list.
- Property change notifications are easy, but when properties depend on others, notifications start to be a bit more tricky: the dependent properties must be handled in the `@property.setter` of the main/original attribute that affects all ohers.

### Events

In this approach to implement an Observer we define an `Event` class derived from `list` which collects callable functions, which are kind of subscribers. In the example, a `Person` is defined with and `Event` type/class for the occasion when he/she falls ill. When that occurs, all the callable subscribers (i.e., functions) from the `Event` are called.

```python
# We have a Person class
# We want an Event to occur, we one Person falls ill
class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.falls_ill = Event()

    def catch_a_cold(self):
        self.falls_ill(self.name, self.address)


# In the Event class, we have subscribers
class Event(list):
    def __call__(self, *args, **kwargs):
        for item in self:
            item(*args, **kwargs)


def call_doctor(name, address):
    print(f'A doctor has been called to {address}')


# __main__
person = Person('Sherlock', '221B Baker St')

# Here, we're accessing Event,
# which is a list of items!
# Each item is a function
# which can be called!
# Here, the callable items just print something
# but similarly, they could perform other tasks,
# e.g., send an email!
person.falls_ill.append(lambda name, addr: print(f'{name} is ill'))
person.falls_ill.append(call_doctor)

# We call the functions by calling the Event
# which is a list of functions = subscribers
person.catch_a_cold()

# And we can remove subscriptions too
person.falls_ill.remove(call_doctor)
# So only one callable item = subscriber = function is run
person.catch_a_cold()

# Sherlock is ill
# A doctor has been called to 221B Baker St
# Sherlock is ill
```

### Property Observers

This example shows how the changes in class attributes can be notified by using the `@property` decorator in Python. Basically, the same `Event` class as before is used via the `@property.setter`.

```python
class Event(list):
    def __call__(self, *args, **kwargs):
        for item in self:
            item(*args, **kwargs)


# Base class which contains an Event class instance
# Person is derived from it!
class PropertyObservable:
    def __init__(self):
        self.property_changed = Event()


# Person is derived from the Observer
# so that we have the Events baked in
class Person(PropertyObservable):
    def __init__(self, age=0):
        super().__init__()
        self._age = age

    @property
    def age(self):
        return self._age

    # In the property setter
    # we trigger the Event
    # which is related to changes in
    # the age attribute
    @age.setter
    def age(self, value):
        if self._age == value:
            return
        self._age = value
        self.property_changed('age', value)


# This class uses the Observer
# to check when people can drive
class TrafficAuthority:
    def __init__(self, person):
        self.person = person
        person.property_changed.append(self.person_changed)

    def person_changed(self, name, value):
        if name == 'age':
            if value < 16:
                print('Sorry, you still cannot drive')
            else:
                print('Okay, you can drive now')
                self.person.property_changed.remove(self.person_changed)

# __main__
p = Person()
ta = TrafficAuthority(p)
for age in range(14, 20):
    print(f'Setting age to {age}')
    p.age = age

# Setting age to 14
# Sorry, you still cannot drive
# Setting age to 15
# Sorry, you still cannot drive
# Setting age to 16
# Okay, you can drive now
# Setting age to 17
# Setting age to 18
# Setting age to 19
```

### Property Dependencies

Property Observers can face difficulties when properties are dependent among them. This example shows how to solve those cases.

```python
class Event(list):
    def __call__(self, *args, **kwargs):
        for item in self:
            item(*args, **kwargs)


class PropertyObservable:
    def __init__(self):
        self.property_changed = Event()


class Person(PropertyObservable):
    def __init__(self, age=0):
        super().__init__()
        self._age = age

    # We add a boolean property to denote whether a Person can vote
    # which clearly depends on the age
    @property
    def can_vote(self):
        return self._age >= 18

    @property
    def age(self):
        return self._age

    # The original property from which the dependent ones
    # hand needs to be modified:
    # We track when the dependent properties change
    # and notify the observer via the Event function calls
    @age.setter
    def age(self, value):
        if self._age == value:
            return

        # We cash the old can_vote
        old_can_vote = self.can_vote

        self._age = value
        self.property_changed('age', value)

        # If the new can_vote is different than the old
        # then, we notify the observer
        if old_can_vote != self.can_vote:
            self.property_changed('can_vote', self.can_vote)

# __main__
def person_changed(name, value):
    if name == 'can_vote':
        print(f'Voting status changed to {value}')

p = Person()
p.property_changed.append(
    person_changed
)

for age in range(16, 21):
    print(f'Changing age to {age}')
    p.age = age

# Changing age to 16
# Changing age to 17
# Changing age to 18
# Voting status changed to True
# Changing age to 19
# Changing age to 20
```

## State (Machine)

Consider an ordinary telephone:

- What you do with it depends on the state of the phone/line
  - If it's ringing or you want to make a call, you can pick it up.
  - The phone must be off the hook to talk/make a call.
  - If you try calling someone and it's busy, you put the handset down.
- Changes in state can be explicit or in response to an event (Observer pattern).

Following the telephone's analogy, the State is a pattern in which the object's behavior is determined by its state. An object transitions from one state to another (something needs to trigger that transition). A formalized construct which manages state and transitions is called a *(finite) state machine*.

The best way of implementing State Machines is to define `State` and `Trigger` classes/enums:

- We define all possible `States`.
- We define all possible events or `Triggers` that can occur.
- We map to each `State` the `Trigger` events that can apply to them and to which `State` they transition when they occur.
- Everything can be packed into a `while` loop where each `State`-`Trigger` pair is checked, and we can sophisticate the logic as we please:
  - Define entry/exit `States`.
  - Gaurd conditions for enabling/disabling transitions.
  - Default action when no transitions are found for an event/`Trigger`.

Notebook: [`Behavioral_Patterns.ipynb`](./04_Behavioral_Patterns/Behavioral_Patterns.ipynb).

### Handmade State Machine

In this example a phone call is modeled with a State Machine. `State` and `Trigger` `Enums` are defined and a `rules` dictionary which maps each current `State` to all possible `(Trigger, NewState)` pairs. Then, we check in a loop the `Trigger` for the current `State` and perform a State Transition associated with each `Trigger`.

```python
from enum import Enum, auto


class State(Enum):
    OFF_HOOK = auto() # handset lifted from the cradle = descolgado
    CONNECTING = auto()
    CONNECTED = auto()
    ON_HOLD = auto()
    ON_HOOK = auto() # handset placed on the cradle = colgado


# Triggers are the things that cause the State transitions
class Trigger(Enum):
    CALL_DIALED = auto()
    HUNG_UP = auto()
    CALL_CONNECTED = auto()
    PLACED_ON_HOLD = auto()
    TAKEN_OFF_HOLD = auto()
    LEFT_MESSAGE = auto()


# __main__
# Now for each State, we need to define which
# Triggers would cause to transition to a new State
# We have a list of pairs for each State:
# (Trigger event, State we transition to)
# Everything is packed in a dictionary Dict[State, List[Trigger, State]]
rules = {
    State.OFF_HOOK: [
        (Trigger.CALL_DIALED, State.CONNECTING)
    ],
    State.CONNECTING: [
        (Trigger.HUNG_UP, State.ON_HOOK),
        (Trigger.CALL_CONNECTED, State.CONNECTED)
    ],
    State.CONNECTED: [
        (Trigger.LEFT_MESSAGE, State.ON_HOOK),
        (Trigger.HUNG_UP, State.ON_HOOK),
        (Trigger.PLACED_ON_HOLD, State.ON_HOLD)
    ],
    State.ON_HOLD: [
        (Trigger.TAKEN_OFF_HOLD, State.CONNECTED),
        (Trigger.HUNG_UP, State.ON_HOOK)
    ]
}

# Starting State: When the State Machine is initiated
state = State.OFF_HOOK
# Ending State; in some State Machines
# exit_state does not occur, e.g., trading bots.
# Here, as soon as a person sets the phone on hook
# we are done!
exit_state = State.ON_HOOK

while state != exit_state:
    print(f'The phone is currently {state}')

    # Check all rules to find current state
    for i in range(len(rules[state])):
        t = rules[state][i][0]
        print(f'{i}: {t}')

    # Request Trigger input
    idx = int(input('Select a trigger:'))
    # Perform State Transiton with Trigger
    s = rules[state][idx][1]
    state = s

print('We are done using the phone.')
# We enter idx in List[] of rules[State], e.g. 0
# The phone is currently State.OFF_HOOK
# 0: Trigger.CALL_DIALED
# The phone is currently State.CONNECTING
# 0: Trigger.HUNG_UP
# 1: Trigger.CALL_CONNECTED
# We are done using the phone.
```

### Switch-Based State Machine

In this example, the State Machine of a lock is implemented following the `switch`-based approach. Python doesn't have a `switch` statement, but we can imlement it using `if-else` or `dicts`.

The advantage of this approach is that we just need to define only `State`, and all the transitions are handled in a `while`-loop. However, it works only for simple State Machines; in complex cases, it is better to define `Triggers` and transition `rules`, as done beforehand.

```python
from enum import Enum, auto


class State(Enum):
    LOCKED = auto()
    FAILED = auto()
    UNLOCKED = auto()


# __main__
code = '1234'
state = State.LOCKED
entry = ''

while True:
    if state == State.LOCKED:
        entry += input(entry)

        if entry == code:
            state = State.UNLOCKED

        if not code.startswith(entry):
            # the code is wrong
            state = State.FAILED
    elif state == State.FAILED:
        print('\nFAILED')
        entry = ''
        state = State.LOCKED
    elif state == State.UNLOCKED:
        print('\nUNLOCKED')
        break
```

## Strategy

Many algorithms can be separated into two layers: high-level and low-level; while high-level deals with the overall goal, the low-level deals with the details. The Strategy makes use of that sepration and enables to select the exact behavior of a system at run-time.

Example: the algorithm of making tea can be decomposed into:

- the process of making a hot beverage (boil water, pout into a cut)
- and tea-specific steps (put teabag into water, etc.)

The high-level algorithm is the one which is reused and provided to the user (prepare hot beverage), who then adds/selects low-level parts (coffe, tea, hot chocolate). Each of the low-level options is called a Strategy, which supports specifics associated with the low-level option:

- Tea-Strategy
- Coffee-Strategy
- Hot-chocolate-Strategy
- etc.

So, in summary, when we use Strategies:

- We define an algorithm at a high level.
- We define the interface we expect each Strategy to follow.
- We provide for dynamic composition of Strategies in the resulting object.

### Example: Text Processor

Notebook: [`Behavioral_Patterns.ipynb`](./04_Behavioral_Patterns/Behavioral_Patterns.ipynb).

This example is a simple text processor which formats a list of bullet points to be in Markdown or HTML. The Strategy pattern is used to specify the low-level text foramtting of the list. That way, we define the high-level code and inject low-level Strategy objects, which are implemented somewhere else. In this case, the Strategy = Format (HTML/Markdown).

```python
from abc import ABC
from enum import Enum, auto


class OutputFormat(Enum):
    MARKDOWN = auto()
    HTML = auto()


# Abstract base class for all Strategies = Formats
# Not required but a good idea
class ListStrategy(ABC):
    def start(self, buffer): pass
    def end(self, buffer): pass
    def add_list_item(self, buffer, item): pass


# Markdown lists are very easy
class MarkdownListStrategy(ListStrategy):

    def add_list_item(self, buffer, item):
        buffer.append(f' * {item}\n')


# HTML lists are a bit more complicated
# bacause they have start/end tags 
# for both the complete list
# and each item
class HtmlListStrategy(ListStrategy):

    def start(self, buffer):
        buffer.append('<ul>\n')

    def end(self, buffer):
        buffer.append('</ul>\n')

    def add_list_item(self, buffer, item):
        buffer.append(f'  <li>{item}</li>\n')


# This text processor is a high-level API
# in which we can choose the low-level Strategy
# i.e., the format, in this case
class TextProcessor:
    def __init__(self, list_strategy=HtmlListStrategy()):
        self.buffer = [] # all the text goes here
        self.list_strategy = list_strategy

    # We add the items of a list, which are appended to the buffer
    def append_list(self, items):
        self.list_strategy.start(self.buffer)
        for item in items:
            self.list_strategy.add_list_item(
                self.buffer, item
            )
        self.list_strategy.end(self.buffer)

    # We set the format at the beginning
    # which instantiates the desired Strategy = Format
    def set_output_format(self, format):
        if format == OutputFormat.MARKDOWN:
            self.list_strategy = MarkdownListStrategy()
        elif format == OutputFormat.HTML:
            self.list_strategy = HtmlListStrategy()

    def clear(self):
        self.buffer.clear()

    def __str__(self):
        return ''.join(self.buffer)

# __main__
items = ['foo', 'bar', 'baz']

tp = TextProcessor()
tp.set_output_format(OutputFormat.MARKDOWN)
tp.append_list(items)
print(tp)
#  * foo
#  * bar
#  * baz

tp.set_output_format(OutputFormat.HTML)
tp.clear()
tp.append_list(items)
print(tp)
# <ul>
#   <li>foo</li>
#   <li>bar</li>
#   <li>baz</li>
# </ul>
```

## Template Method

A Template is a high-level blueprint for an algorithm to be completed by inheritors. In other words, it is equivalent to the Strategy method, but it's implemented via inheritance: it allows us to define the skeleton of the algorithm with concrete implementations defined in subclasses.

- Algorithms can be decomposed into common parts (high-level) + specifics (low-level).
- The Strategy pattern accomplishes the separation of high/low-level parts throuhg composition:
  - High-level algorithm expects strateges to conform to an interface.
  - Concrete implementations implement this interface and are used.
- The Template Method pattern does the same thing as Strategy, but using inheritance
  - The overall algorithm is defined in the base class; it uses abstract members.
  - Inheritors override the abstract members.
  - Template method invoked to get the work done.

The Template Method is usually defined in the base class and not overriden in derived concrete classes; instead, the abstract methods used by it are overriden. That way, the high-level logic is already defined in the Template Method of the base class.

### Example: Chess Game

```python
from abc import ABC


# Our base class = our Skeleton
# It defines the structure of any/many game/s
class Game(ABC):

    def __init__(self, number_of_players):
        self.number_of_players = number_of_players
        self.current_player = 0

    # This is the Template Method!
    def run(self):
        self.start()
        while not self.have_winner:
            self.take_turn()
        print(f'Player {self.winning_player} wins!')

    def start(self): pass

    @property
    def have_winner(self): pass

    def take_turn(self): pass

    @property
    def winning_player(self): pass


# This is our inherited class.
# We won't override our Template Method (run)
# but instead, all the other methods used 
# by it: have_winner, take_turn, winning_player
class Chess(Game):
    def __init__(self):
        super().__init__(2)
        self.max_turns = 10
        self.turn = 1

    def start(self):
        print(f'Starting a game of chess with {self.number_of_players} players.')

    @property
    def have_winner(self):
        return self.turn == self.max_turns

    def take_turn(self):
        print(f'Turn {self.turn} taken by player {self.current_player}')
        self.turn += 1
        self.current_player = 1 - self.current_player

    @property
    def winning_player(self):
        return self.current_player

# __main__
chess = Chess()
chess.run()
# Starting a game of chess with 2 players.
# Turn 1 taken by player 0
# Turn 2 taken by player 1
# Turn 3 taken by player 0
# Turn 4 taken by player 1
# Turn 5 taken by player 0
# Turn 6 taken by player 1
# Turn 7 taken by player 0
# Turn 8 taken by player 1
# Turn 9 taken by player 0
# Player 1 wins!
```
