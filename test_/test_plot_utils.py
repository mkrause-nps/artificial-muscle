#!/usr/bin/env python3

from src.plot_utils import PlotUtils
import unittest


class TestPlotUtils(unittest.TestCase):

    def setUp(self):
        self.tups = [(1, 'a'), (2, 'b'), (3, 'c')]
        self.lst1 = [1, 2, 3]
        self.lst2 = ['a', 'b', 'c']

    def test_lst_tuples_to_list(self):
        observed = PlotUtils.lst_tuples_to_lists(self.tups)
        expected = (self.lst1, self.lst2)
        self.assertEqual(expected, observed)


if __name__ == '__main__':
    unittest.main()
