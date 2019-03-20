#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_sample.py
This is a sample test module.
"""
from parameterized import parameterized
import unittest
import process_checker


class ParameterizedExampleTestSuite(unittest.TestCase):
    """
    Test process checker
    """
    @parameterized.expand([
        (1, 2, 5),
        (3, 4, 25)
    ])
    def test_ab_addSquares_equalsC(self, a, b, c):
        """
        example.
        :param a: the first parameter
        :param b: the second parameter
        :param c: the result of adding the squares of a and b
        """
        self.assertEqual(c, a*a + b*b)
