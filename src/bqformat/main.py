import argparse
import re
import sys
from enum import Enum
from pathlib import Path
from typing import Container, NamedTuple


class _Dictionary(Enum):
    WORDS = "words.txt"
    STOPWORDS = "stopwords.txt"

    def read(self) -> Container[str]:
        path = Path(__file__).parent / "data" / self.value
        with path.open() as f:
            # remove '\n'
            return frozenset(line[:-1] for line in f.readlines())


class Column(NamedTuple):
    column_name: str

    @property
    def report(self):
        if 0.5 <= self.score:
            return None
        return f"The column name '{self.column_name}' should be more meaningful."

    @property
    def score(self) -> float:
        dictionary = _Dictionary.WORDS.read()
        stopwords = _Dictionary.STOPWORDS.read()

        words = {
            word
            for word in re.split(r"[^a-z]+", self.column_name.lower())
            if word not in stopwords
        }
        length = len(words)
        if length == 0:
            return 0
        return sum(1 for word in words if word in dictionary) / length


class SQL(NamedTuple):
    query: str

    @property
    def formatted(self):
        return self.query

    def _find_columns(self):
        for m in re.finditer(r"(?<=AS )\w+", self.query):
            column_name = m.group()
            yield Column(column_name)

    @property
    def reports(self):
        for column in self._find_columns():
            if column.report:
                yield column


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sql", type=argparse.FileType("r"), default="-")
    args = parser.parse_args()
    sql = SQL(args.sql.read())
    reports = list(sql.reports)
    if reports:
        for column in reports:
            print(column.report, file=sys.stderr)
        sys.exit(1)

    print(sql.formatted)


if __name__ == "__main__":
    main()
