from datetime import date

from pydining.client.functions import meals_by_period
from pydining.client.models import Connection, Meal


def test_meals_by_period(connection: Connection):
    meals = meals_by_period(connection, date.today(), date.today())

    assert len(meals) == 6
    assert isinstance(meals, list)
    assert all(isinstance(meal, Meal) for meal in meals)
