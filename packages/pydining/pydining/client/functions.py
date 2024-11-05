from datetime import date

import requests

from pydining.client.models import Connection

from .models import Meals

def meals_by_period(connection: Connection, start: date, end: date):
    response = requests.get(f"{connection.url}/v1/menus/period/{start.strftime("%Y%m%d")}/{end.strftime("%Y%m%d")}")
    response.raise_for_status()

    return Meals.validate_json(response.text)
