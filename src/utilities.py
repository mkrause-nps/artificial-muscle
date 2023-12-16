#!/usr/bin/env python3

import os


class Utilities:

    @staticmethod
    def get_filename_from_path(absolute_file_path: str):
        return os.path.splitext(os.path.basename(absolute_file_path))[0]

    @staticmethod
    def get_project_root() -> str:
        """Get the absolute path of the project root."""
        current_path = os.path.abspath(__file__)  # Get the absolute path of the current script
        project_root = os.path.dirname(os.path.dirname(current_path))  # Go up two levels to reach the project root
        return project_root

    @staticmethod
    def get_filename_list(start_path: str) -> list[str]:
        """Get a list of all absolute filenames, recursively, from directory start_path."""
        file_list: list = []
        for root, dirs, files in os.walk(start_path):
            for file in files:
                file_list.append(os.path.join(root, file))

        return file_list
