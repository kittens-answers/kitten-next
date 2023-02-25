from dataclasses import dataclass


class Specification:
    ...


@dataclass(frozen=True)
class TextContains(Specification):
    q: str
