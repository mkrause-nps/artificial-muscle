#!/usr/bin/env python3
from src.loader_interface import LoaderInterface
from src.config import Config
import pandas as pd


class AmScopeExcelLoader(LoaderInterface):
    @classmethod
    def load(cls, filename: str) -> list[dict]:
        df = pd.read_excel(filename, sheet_name=Config.py_all)
        return df.to_dict('records')
