"""From the Udemy course "Design Patterns in Python"
https://www.udemy.com/course/design-patterns-python
by Dmitri Nesteruk.

Creational Patterns: Singleton
"""
from unittest import TestCase
from copy import deepcopy

def is_singleton(factory):
    x = factory()
    y = factory()
    return x is y

class Evaluate(TestCase):
    def test_exercise(self):
        obj = [1, 2, 3]
        self.assertTrue(is_singleton(lambda: obj))
        self.assertFalse(is_singleton(lambda: deepcopy(obj)))