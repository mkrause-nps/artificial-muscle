#!/usr/bin/env python3
import unittest

from src.analise_thesis.plotter import Plotter


class TestPlotter(unittest.TestCase):

    def setUp(self):
        data_hard = [
            (100, 1, 'hard'),
            (200, 1, 'hard'),
            (100, 2, 'hard'),
            (100, 3, 'hard'),
        ]

        self.plotter_test = Plotter(data=data_hard, nrows=1, ncols=1,
                                    xlabel="injection number", ylabel='R [K$\Omega$]',
                                    xlim=[0, 5], ylim=[0, 1e6], capsize=10)

    def test_filter_by_width(self):
        data_from_single_channel_width = self.plotter_test.filter_by_width(width=100)
        expected = [(100, 1, 'hard'), (100, 2, 'hard'), (100, 3, 'hard')]
        self.assertEqual(expected, data_from_single_channel_width)

    def test_get_channel_list(self):
        channels = self.plotter_test.get_channel_list()
        expected = [100, 200]
        self.assertEqual(expected, channels)


if __name__ == '__main__':
    unittest.main()
