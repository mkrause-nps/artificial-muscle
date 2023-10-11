#!/usr/bin/env python3
import math


class WeightedAverage:
    """Returns weighted average and standard deviation of multiple means and standard deviations"""

    means = None
    stddevs = None
    weights = None
    variances = None
    float_zero = 0.0
    # If the resistance value was the instrument's out-of-range-value, its standard deviation is 0. In that case, we
    # have to set an arbitrary standard deviation to avoid division by 0 errors. It is an attempted reasonable guess.
    ASSUMED_STDEV_FOR_OUT_OF_RANGE = 10.0

    @classmethod
    def get(cls, data: list[tuple]) -> tuple:
        """
        @param data: list of 2-tuples, where the first tuple is a list of means and the second a list of standard
                        deviations
        @return: a 2-tuple where the first value is the weighted mean, the second the weighted standard
                        deviation
        """
        if not isinstance(data, list):
            raise ValueError('input data must be a list')

        cls.__get_means_stddevs(data=data)
        cls.__compute_weights()

        wsm: float = cls.__sum_weighted_means()
        sows: float = cls.__sum_weights()
        try:
            weighted_average: float = wsm / sows
        except ZeroDivisionError:
            print('Sum of Weights is 0...')
            weighted_average = wsm
        wsv = cls.__sum_weighted_variances()
        try:
            grand_variance = wsv / (sows * sows)
        except ZeroDivisionError:
            grand_variance = wsv
        weighted_stddev = math.sqrt(grand_variance)

        return weighted_average, weighted_stddev

    @classmethod
    def __get_means_stddevs(cls, data: list[tuple]) -> None:
        """Create means and stddevs as class variables"""
        try:
            means_tup, stddevs_tup = list(zip(*data))
            cls.means: list = list(means_tup)
            if cls.__array_contains_zeros(list(stddevs_tup)):
                cls.stddevs = list(
                    map(lambda x: x + cls.ASSUMED_STDEV_FOR_OUT_OF_RANGE if x == 0.0 else x, list(stddevs_tup)))
            else:
                cls.stddevs: list = list(stddevs_tup)
        except ValueError:
            print(f'data seems to be empty: {len(data)}')

    @classmethod
    def __sum_weighted_means(cls) -> float:
        """Return sum of weighted means (swm)"""
        if len(cls.means) != len(cls.weights):
            print(f'means: {cls.means}')
            print(f'weights: {cls.weights}')
            raise ValueError("Lists of means and weights need to have the same number of elements")
        return sum(cls.__multiply_lists_elementwise(u=cls.means, v=cls.weights))

    @classmethod
    def __compute_weights(cls) -> None:
        """Compute a list of weights corresponding to a standard deviation as a class variable"""
        print(f'stddevs: {cls.stddevs}')
        try:
            cls.weights: list[float] = [1 / (sigma * sigma) for sigma in cls.stddevs]
        except ZeroDivisionError:
            print(f'The standard deviation seems to contain value 0.0: {cls.stddevs}')

    @classmethod
    def __sum_weights(cls) -> float:
        """Return sum of weights (sows)"""
        print(f'cls.weights: {cls.weights}')
        return sum(cls.weights)

    @classmethod
    def __weighted_variances(cls) -> list:
        """Return array of weighted variances (var_w)"""
        if cls.weights is None:
            cls.__compute_weights()
        if cls.variances is None:
            cls.__get_variances()
        return list(map(lambda tup: tup[0] * tup[1], list(zip(cls.weights, cls.variances))))

    @classmethod
    def __sum_weighted_variances(cls) -> float:
        """Return sum of weighted variances (swv)"""
        return sum(cls.__weighted_variances())

    @classmethod
    def __get_variances(cls):
        """Create list of variances as class variable"""
        cls.variances = [stddev * stddev for stddev in cls.stddevs]

    @staticmethod
    def __multiply_lists_elementwise(u: list, v: list) -> list:
        """Return the product of two lists elementwise"""
        return list(map(lambda tup: tup[0] * tup[1], list(zip(u, v))))

    @classmethod
    def __array_contains_zeros(cls, arr: list):
        return cls.float_zero in arr
