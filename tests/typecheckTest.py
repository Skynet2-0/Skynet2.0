"""
Created June 10, 2016

@author: Stefan
"""

import unittest
from typing.typecheck import *


class TypeCheckTest(unittest.TestCase):
    """
    Checks the typechecker.
    """

    #def __init__(self):
    #    super(self, TypeCheckTest).__init__()

    def testCheckTypeFloat(self):
        self.assertTrue(check_type(1.0, float))

    def testCheckTypeInt(self):
        self.assertTrue(check_type(1, int))

    def testCheckTypeStringIsUnittest(self):
        with self.assertRaises(TypeError):
            check_type("xjSLA.fiv", unittest.TestCase)

    def testCheckTypeTypeCheckTestIsUnittest(self):
        self.assertTrue(check_type(TypeCheckTest(), unittest.TestCase))

    def testPositiveInteger1(self):
        self.assertTrue(check_positive(1))

    def testPositiveMinus4(self):
        with self.assertRaises(ValueError):
            check_positive(-4)

    def testPositive0(self):
        self.assertTrue(check_positive(0))

    def testPositiveComplex(self):
        with self.assertRaises(TypeError):
            check_positive(complex(2, 1)) # Complex numbers do not have < operator.

    def testCheckPositiveFloatOfFloat1(self):
        self.assertTrue(check_positive_float(1.0))

    def testCheckPositiveFloatOfFloatMinus1(self):
        with self.assertRaises(ValueError):
            check_positive_float(-1.0)

    def testCheckPositiveFloatOfInteger1(self):
        with self.assertRaises(TypeError):
            check_positive_float(1)

    def testCheckPositiveFloatString(self):
        with self.assertRaises(TypeError):
            check_positive_float("XykAKSL")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
