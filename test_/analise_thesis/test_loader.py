#!/usr/bin/env python3

import os
import pandas as pd
from src.analise_thesis.loader import Loader
from test_.analise_thesis.set_up import SetUp


class TestLoader(SetUp):
    def test_write_to_json(self) -> None:
        Loader.write_to_json(df=self.df, dst=self.test_data_path)
        is_file_exist = True
        f_name = os.path.join(self.test_data_path, self.test_json_filename)
        file_obj = ''
        try:
            file_obj = open(file=f_name, mode='r')
        except FileNotFoundError:
            is_file_exist = False
        finally:
            file_obj.close()

        self.assertEqual(True, is_file_exist)

    def test_read_data_file_not_found(self) -> None:
        df = Loader.read_data(data_path=self.test_data_filename_not_exists, sheet_name='foo')
        self.assertEqual(df, None)

    def test_read_data(self) -> None:
        df = Loader.read_data(self.test_data_path, sheet_name=self.test_data_sheet1_name)
        print(df)
        pd.testing.assert_frame_equal(self.df2, df)


# if __name__ == '__main__':
#     unittest.main()
