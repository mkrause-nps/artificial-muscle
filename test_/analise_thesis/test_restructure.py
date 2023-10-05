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

    def test_restructure_idx_0(self):
        idx = 0
        expected = ([197.1, 308.3, 220000.0], [0.08433, 463.7, 0.01505])
        observed = Restructure.restructure(tup=(self.data_a, self.data_b, self.data_c), idx=idx)
        self.assertEqual(expected, observed)

    def test_restructure_idx_3(self):
        idx = 3
        expected = ([15.12, 20.88], [0.03313, 0.02703])
        observed = Restructure.restructure(tup=(self.data_a, self.data_b, self.data_c), idx=idx)
        self.assertEqual(expected, observed)

    def test_restructure_idx_4(self):
        """Testing out-of-range index for any list in tuple"""
        idx = 4
        expected = ([], [])
        observed = Restructure.restructure(tup=(self.data_a, self.data_b, self.data_c), idx=idx)
        self.assertEqual(expected, observed)



if __name__ == '__main__':
    unittest.main()
