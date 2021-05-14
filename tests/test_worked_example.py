import pytest

from dataclasses import dataclass, asdict
from src.diversity_inclusion_metrics import DIMetrics


"""
We begin with the context and person creating the query. 
The person may be seeking a selection of stock images to 
use for a presentation to an unknown-to-them audience. 
The person has a token p in the system where they permit 
information to be stored, such as their gender and hair color. 
"""

di: DIMetrics = DIMetrics()

@dataclass
class WorkedExample:
    gender: float
    skin: int
    age: int
    # hair: dict TODO

    @staticmethod
    def representativeness_gender(Xi, Pi) -> float:
        # i_("gender ")-=p_("gender ")
        return 1.00 if Xi == Pi else 0.00

    @staticmethod
    def representativeness_skin(Xi, Pi) -> float:
        # MAX_(skin)-(d(i_(skin),p_(skin)))/(MAX_(skin))
        return Xi / Pi # TODO investigate formula

    @staticmethod
    def representativeness_age(Xi, Pi, max_age: int = 100) -> float:
        # (d(" age "_(i)," age "_(p)))/(MAX_(age))
        return 1 - (abs(Xi - Pi) / max_age)


fixture_p: dict = WorkedExample(1.00, 6, 70)

fixture_X: list = [
    WorkedExample(1.00, 5, 31),
    WorkedExample(1.00, 4, 23),
    WorkedExample(1.00, 3, 47),
]

query: str = "scientist"


@pytest.fixture
def all_scores(Xi: list = fixture_X, Pi: dict = fixture_p) -> list:
    all_scores: list = []
    for i in Xi:
        scores = di.representativeness(i, Pi) #, "scientist")
        all_scores.append(scores)
    return all_scores


def test_representativeness(all_scores: list):
    assert [[round(n, 2) for n in x] for x in all_scores] == [
        [1.0, 0.83, 0.61],
        [1.0, 0.67, 0.53],
        [1.0, 0.50, 0.77],
    ]


def test_utilitarian(all_scores: list):
    res = di.utilitarian_inclusivity(all_scores)
    assert [round(x, 2) for x in res] == [0.81, 0.73, 0.76]


def test_nash(all_scores: list):
    res = di.nash_inclusivity(all_scores)
    assert [round(x, 2) for x in res] == [0.8, 0.71, 0.73]  # 0.79, 0.71, 0.73


def test_egalitarian(all_scores: list) -> list:
    res = di.egalitarian_inclusivity(all_scores)
    assert [round(x, 2) for x in res] == [0.61, 0.53, 0.50]
