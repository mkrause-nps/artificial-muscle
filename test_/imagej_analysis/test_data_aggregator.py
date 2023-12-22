#!/usr/bin/env python3
import unittest
from test_.imagej_analysis.test_imagej_csv_base_class import TestImageJCsvBaseClass
from src.imagej_analysis.data_aggregator import DataAggregator


class TestDataAggregator(TestImageJCsvBaseClass):
    def test_list_csv_files(self):
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
