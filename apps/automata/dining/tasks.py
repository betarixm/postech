from datetime import date
from typing import Any

import requests
from pydining.client.functions import meals_by_period
from pydining.client.models import Connection as _Connection

from automata.celery import app


@app.task
def notify_today_meals_on_discord(webhook_url: str):
    today = date.today()

    meals = meals_by_period(
        _Connection(protocol="https", host="food.podac.poapper.com", port=443),
        today,
        today,
    )

    message: dict[str, Any] = {
        "content": "",
        "tts": False,
        "embeds": [
            {
                "title": today.strftime("%Y. %m. %d. (%A)"),
                "color": 2326507,
                "fields": [
                    {
                        "name": meal.type,
                        "value": "\n".join(f"- {food.name}" for food in meal.foods),
                        "inline": False,
                    }
                    for meal in meals
                ],
            }
        ],
        "components": [],
        "actions": {},
        "username": "automata",
    }

    requests.post(webhook_url, json=message)
