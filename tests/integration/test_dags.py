import os
from typing import Generator

import pytest
from airflow.models.dagbag import DagBag


@pytest.fixture
def dag_bag() -> Generator:
    dag_folder = "dags"
    os.environ["ENV"] = "development"
    yield DagBag(dag_folder=dag_folder, include_examples=False)


def test_dags_load_with_no_errors(dag_bag: DagBag) -> None:
    assert not dag_bag.import_errors


def test_expected_dags_are_loaded(dag_bag: DagBag) -> None:
    assert list(dag_bag.dags.keys()) == ["dummy"]
