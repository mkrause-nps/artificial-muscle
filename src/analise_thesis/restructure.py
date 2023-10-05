#!/usr/bin/env python3

class Restructure:

    idx_ydata: int = 0
    idx_err: int = 1
    minimum_number_elements: int = 0

    @classmethod
    def restructure(cls, tup: tuple, idx: int) -> tuple[list, list]:
        """Return a tuple of lists

        @param tup: Tuple of tuples, each of which contains two lists. The first of those lists contains
                    y-data, and the second corresponding y-errors. Both lists have the same length.
        such that the
        @param idx: The index of the list
        @return: A tuple of two lists. The first list contains all the idx-th element of the y-data, the second
                    list contains all the idx-th element of the y-errors.
        """

        tup = cls.__triage_if_idx_out_of_range(tup=tup, idx=idx)

        return (
            list(map(lambda x: x[cls.idx_ydata][idx], tup)),
            list(map(lambda x: x[cls.idx_err][idx], tup))
        )

    @classmethod
    def __triage_if_idx_out_of_range(cls, tup: tuple, idx: int):
        groomed_data = []
        for tupl in tup:
            try:
                tupl[cls.idx_ydata][idx]
            except IndexError:
                print('skipping...')
                continue
            groomed_data.append((tupl[cls.idx_ydata], tupl[cls.idx_err]))

        return tuple(groomed_data)

    @classmethod
    def __get_minimum_number_elements(cls, tup: tuple) -> None:
        cls.minimum_number_elements = min([len(tup[idx][0]) for idx in range(len(tup))])


if __name__ == '__main__':
    pass
