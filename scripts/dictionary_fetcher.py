import shutil
import tempfile
import urllib.request
from os import PathLike
from pathlib import Path
from typing import Sequence

import openpyxl


def fetch_new_gsl():
    with tempfile.NamedTemporaryFile(suffix=".xlsx") as tmp_file:
        with urllib.request.urlopen(
            "http://www.newgeneralservicelist.org/s/NGSL-WordList-101-alphabetized.xlsx"
        ) as response:
            shutil.copyfileobj(response, tmp_file)

        wb = openpyxl.load_workbook(tmp_file.name)
        ws = wb["NGSL"]
        values = iter(ws.values)
        # skip column name
        next(values)
        for value in values:
            # first column
            yield value[0].lower()


def fetch_new_awl():
    with urllib.request.urlopen(
        "http://www.newgeneralservicelist.org/s/NAWL_Headwords.txt"
    ) as response:
        for line in response:
            # remove b'\r\n'
            yield line[:-2].decode("utf-8").lower()


def fetch_stopwords():
    with urllib.request.urlopen(
        "https://raw.githubusercontent.com/stanfordnlp/CoreNLP/master/data/edu/stanford/nlp/patterns/surface/stopwords.txt"
    ) as response:
        for line in response:
            # remove b'\n'
            yield line[:-1].decode("utf-8").lower()


def _write_dictionary(dictionary: Sequence[str], file: PathLike):
    with file.open("w") as f:
        f.writelines(line + "\n" for line in dictionary)


def prepare_dictionary():
    ngsl = frozenset(fetch_new_gsl())
    nawl = frozenset(fetch_new_awl())
    words = sorted(ngsl | nawl)
    path = Path(__file__).parent.parent / "src/bqformat/data"
    path.mkdir(parents=True, exist_ok=True)
    _write_dictionary(words, path / "words.txt")

    stopwords = sorted(frozenset(fetch_stopwords()))
    _write_dictionary(stopwords, path / "stopwords.txt")


if __name__ == "__main__":
    prepare_dictionary()
