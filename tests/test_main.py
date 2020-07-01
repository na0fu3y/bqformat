import pytest

from src.bqformat.main import SQL, Column, QuerySyntaxError


def test_sql_formatted():
    assert SQL("select 1 a").formatted == "SELECT\n  1 AS a;\n"


def test_sql_formatted_failure():
    with pytest.raises(QuerySyntaxError):
        _ = SQL("select 1a").formatted


def test_sql_reports():
    assert sum(1 for _ in SQL("SELECT 1 AS a, 'STRING' AS str").reports) == 2


@pytest.mark.parametrize(
    "column_name, expected_min, expected_max",
    [("a", 0.0, 0.0), ("sample_score", 0.1, 1.0),],
)
def test_column_score(column_name, expected_min, expected_max):
    assert expected_min <= Column(column_name).score <= expected_max
