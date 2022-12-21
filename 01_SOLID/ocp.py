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

if __name__ == "__main__":

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