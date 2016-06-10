"""
Module that unifies the type checking of various variables if it is done at all.

Created June 10th, 2016

@author: Stefan
"""


def check_type(var, vartype):
    """
    Checks if the type of var is vartype and raises an error if not.

    var -- the variable to check the type of.
    vartype -- The expected type.
    raises TypeError -- If var is not of type type.
    return True -- If succesfull.
    """
    if not isinstance(var, vartype):
        raise TypeError(str(value) + " is not of the required type " + str(vartype))
    return True

def check_positive(var):
    """
    Checks whether var is positive or not.

    var -- The variable of a number type to check.
    raises ValueError -- If the value of var is negative.
    return True -- If the check is succesfull.
    """
    if var < 0:
        raise ValueError("Variable is not positive but should be.")
    return True


def check_positive_float(var):
    """
    Checks if var is a positive float.

    var -- The variable to check.
    raises TypeError -- If var is not a float
    raises ValueError -- If var is negative.
    returns True -- If the test is succesfull.
    """
    check_type(var, float)
    return check_positive(var)
