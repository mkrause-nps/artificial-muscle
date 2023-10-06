#!/usr/bin/env python3

import unittest
from src.analise_thesis.restructure import Restructure


class TestRestructure(unittest.TestCase):

    def setUp(self):
        ydata = [197.1, 39.86, 35.06, 15.12]
        yerr = [0.08433, 0.6405, 2.943, 0.03313]
        self.data_a: tuple = (ydata, yerr)

        ydata = [308.3, 31.83, 26.15]
        yerr = [463.7, 75.78, 794.6]
        self.data_b: tuple = (ydata, yerr)

        ydata = [220000.0, 94.51, 26.97, 20.88]
        yerr = [0.01505, 0.2285, 0.008552, 0.02703]
        self.data_c: tuple = (ydata, yerr)

        self.tups = (
            ([197.1, 39.86, 35.06, 15.12], [0.08433, 0.6405, 2.943, 0.03313]),
            ([308.3, 31.83, 26.15], [463.7, 75.78, 794.6]),
            ([220000.0, 94.51, 26.97, 20.88], [0.01505, 0.2285, 0.008552, 0.02703])
        )

    def test_restructure_idx(self):
        idx = 0
        expected = [
            [(197.1, 0.08433), (308.3, 463.7), (220000.0, 0.01505)],
            [(39.86, 0.6405), (31.83, 75.78), (94.51, 0.2285)],
            [(35.06, 2.943), (26.15, 794.6), (26.97, 0.008552)],
            [(15.12, 0.03313), (20.88, 0.02703)]
        ]
        observed = Restructure.restructure(tups=(self.data_a, self.data_b, self.data_c))
        self.assertEqual(expected, observed)

    def test_get_minimum_number_elements(self):
        Restructure._Restructure__get_minimum_number_elements(self.tups)
        observed = Restructure.minimum_number_elements
        expected = 3
        self.assertEqual(expected, observed)

    def test_get_maximum_number_elements(self):
        Restructure._Restructure__get_maximum_number_elements(self.tups)
        observed = Restructure.maximum_number_elements
        expected = 4
        self.assertEqual(expected, observed)


if __name__ == '__main__':
    unittest.main()
