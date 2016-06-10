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
        self.assertTrue(check_positive(-4))

    def testPositiveComplexNumber(self):
        complex_number = complex(2, 1)
        self.assertTrue(check_positive(complex_number))

    def testPositiveComplexNumber2(self):
        complex_number = complex(2, -1)
        self.assertTrue(check_positive(complex_number))

    def testPositiveComplexNumber3(self):
        complex_number = complex(-2, 1)
        self.assertTrue(check_positive(complex_number))

    def testPositiveComplexNumber4(self):
        complex_number = complex(-2, -1)
        with self.assertRaises(ValueError):
            self.check_positive(complex_number)

    def testPositiveComplexNumber2(self):
        complex_number = complex(0, 1)
        self.assertTrue(check_positive(complex_number))

    def testPositiveString(self):
        with self.assertRaises(Exception):
            self.check_positive("jsConsa997")

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
