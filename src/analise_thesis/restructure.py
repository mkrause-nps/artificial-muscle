#!/usr/bin/env python3

class Restructure:

    idx_ydata: int = 0
    idx_err: int = 1
    minimum_number_elements: int = 0
    maximum_number_elements: int = 0

    @classmethod
    def restructure(cls, tups: tuple) -> list:
        """Return a list of lists, where data are restructured to match the input for WeightedAverage.get.

        @param tups:    Tuple of tuples. Each innter tuple contains two lists. The first of those lists contains
                        y-data, and the second corresponding y-errors. Both lists have the same length.
        @return:        A list of lists. Each inner list corresponds to one x-value. The inner list contains
                        2-tuples representing replications of an experiment where the first element of each
                        2-tuple corresponds to the y-data value and the second to the y-error
        """

        restructured_data = []
        cls.__get_maximum_number_elements(tups=tups)
        if cls.maximum_number_elements == 0:
            return restructured_data
        x_idx_list = cls.__get_x_idx()
        for x_idx in x_idx_list:
            groomed_tups = cls.__triage_if_idx_out_of_range(tups=tups, idx=x_idx)
            restructured_data.append(
                list(map(lambda x: (x[cls.idx_ydata][x_idx], x[cls.idx_err][x_idx]), groomed_tups))
            )

        return restructured_data

    @classmethod
    def __triage_if_idx_out_of_range(cls, tups: tuple, idx: int) -> tuple:
        """Removes lists from tups that a shorted than length idx and returns tuple"""
        groomed_data = []
        for tup in tups:
            try:
                tup[cls.idx_ydata][idx]
            except IndexError:
                print('skipping...')
                continue
            groomed_data.append((tup[cls.idx_ydata], tup[cls.idx_err]))

        return tuple(groomed_data)

    @classmethod
    def __get_minimum_number_elements(cls, tups: tuple) -> None:
        cls.minimum_number_elements = min([len(tups[idx][0]) for idx in range(len(tups))])

    @classmethod
    def __get_maximum_number_elements(cls, tups: tuple) -> None:
        try:
            cls.maximum_number_elements = max([len(tups[idx][0]) for idx in range(len(tups))])
        except ValueError:
            print(f'tups seems to be empty: {len(tups)}')

    @classmethod
    def __get_x_idx(cls) -> list:
        return list(range(0, cls.maximum_number_elements))


if __name__ == '__main__':
    pass
