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

