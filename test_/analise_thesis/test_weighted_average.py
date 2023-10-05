#!/usr/bin/env python3

import unittest
from src.analise_thesis.weighted_average import WeightedAverage


class TestWeightedAverage(unittest.TestCase):

    def setUp(self):
        self.means = [3, 2, 5]
        self.stddevs = [0.2, 0.2, 0.4]
        self.data = list(zip(self.means, self.stddevs))
        self.weights = [1/0.04, 1/0.04, 1/0.16]
        self.weighted_variances = [0.004444444444444445, 0.01, 0.0064]

    def test_get(self):
        expected_average = 2.777777777
        expected_stddev = 0.030792014356780046
        observed_average, observed_stddev = WeightedAverage.get(self.data)
        self.assertAlmostEqual(expected_average, observed_average)
        self.assertAlmostEqual(expected_stddev, observed_stddev)

    def test_sum_weighted_means(self):
        WeightedAverage._WeightedAverage__get_means_stddevs(self.data)
        WeightedAverage._WeightedAverage__compute_weights()
        observed = WeightedAverage._WeightedAverage__sum_weighted_means()
        expected = 156.25
        self.assertAlmostEqual(expected, observed)

    def test_compute_weights(self):
        expected = self.weights
        WeightedAverage._WeightedAverage__get_means_stddevs(self.data)
        WeightedAverage._WeightedAverage__compute_weights()
        observed = WeightedAverage.weights
        for e, o in zip(expected, observed):
            self.assertAlmostEqual(e, o)

    def test_sum_weights(self):
        WeightedAverage._WeightedAverage__get_means_stddevs(self.data)
        WeightedAverage._WeightedAverage__compute_weights()
        observed = WeightedAverage._WeightedAverage__sum_weights()
        expected = 56.25
        self.assertAlmostEqual(expected, observed)

    def test_weighted_variances(self):
        WeightedAverage._WeightedAverage__get_means_stddevs(self.data)
        observed = WeightedAverage._WeightedAverage__weighted_variances()
        print(observed)
        expected = [1.0, 1.0, 1.0]
        for e, o in zip(expected, observed):
            self.assertAlmostEqual(e, o)

    def test_sum_weighted_variances(self):
        WeightedAverage._WeightedAverage__get_means_stddevs(self.data)
        observed = WeightedAverage._WeightedAverage__sum_weighted_variances()
        expected = sum([1.0, 1.0, 1.0])
        self.assertAlmostEqual(expected, observed)

    def test_multiply_lists_elementwise(self):
        observed = WeightedAverage._WeightedAverage__multiply_lists_elementwise(self.means, self.weights)
        expected = [75, 50, 31.25]
        for e, o in zip(expected, observed):
            self.assertAlmostEqual(e, o)


if __name__ == '__main__':
    unittest.main()
