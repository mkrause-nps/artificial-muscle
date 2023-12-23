#!/usr/bin/env python3


class LoaderInterface:

    @classmethod
    def load(cls, filename: str) -> list[dict]:
        raise NotImplementedError("Subclasses must implement this method")
