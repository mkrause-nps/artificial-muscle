#!/usr/bin/env python3
import unittest
from test_imagej_csv_base_class import TestImageJCsvBaseClass
from src.imagej_analysis.imagej_csv_loader import ImageJCsvLoader


class TestImageJCsvLoader(TestImageJCsvBaseClass):
    def test_load(self):
        data: list[dict] = ImageJCsvLoader.load(filename=self.test_csv_file)
        self.assertEqual(self.expected_output_from_load, data)

    @unittest.skip("Not implemented")
    def test_list_csv_files(self):
        pass


if __name__ == '__main__':
    unittest.main()
