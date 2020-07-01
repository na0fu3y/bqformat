import argparse
import itertools
import re
import subprocess
import sys
from enum import Enum
from pathlib import Path
from typing import Container, NamedTuple


class QuerySyntaxError(Exception):
    pass


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

    @staticmethod
    def pairwise(iterable):
        """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)

    @property
    def formatted(self):
        try:
            return subprocess.run(
                ["/format_sql"],
                input=self.query.encode("utf-8"),
                check=True,
                capture_output=True,
            ).stdout.decode("utf-8")
        except subprocess.CalledProcessError as e:
            raise QuerySyntaxError(e.stderr)

    def _find_aliases(self):
        out = subprocess.run(
            ["/parse_statement"],
            input=self.query.encode("utf-8"),
            check=True,
            capture_output=True,
        ).stdout.decode("utf-8")
        pattern_alias = re.compile(r" +Alias \[\d+-\d+\]")
        pattern_identifier = re.compile(r" +Identifier\((.+)\) \[\d+-\d+\]")

        for previous, current in SQL.pairwise(out.split("\n")):
            if not pattern_alias.fullmatch(previous):
                continue
            m = pattern_identifier.fullmatch(current)
            if m is None:
                raise QuerySyntaxError(f"The alias must come before an identifier")
            if pattern_alias.fullmatch(previous):
                yield Column(m.group(1))

    @property
    def reports(self):
        for column in self._find_aliases():
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
