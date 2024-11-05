from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, TypeAdapter, model_validator


class Connection(BaseModel):
    protocol: Literal["http", "https"]
    host: str
    port: int

    @property
    def url(self) -> str:
        return f"{self.protocol}://{self.host}:{self.port}"


class Food(BaseModel):
    id: int
    name: str
    is_vegan: bool
    is_main: bool

    @model_validator(mode="before")
    @classmethod
    def from_response(cls, values: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": values["id"],
            "name": values["name_kor"],
            "is_vegan": values["isVegan"],
            "is_main": values["isMain"],
        }


class Meal(BaseModel):
    id: int
    date: date
    type: Literal[
        "breakfast-a", "breakfast-b", "lunch", "dinner", "staff", "international"
    ]
    kcal: int
    protein: int
    foods: list[Food]

    @model_validator(mode="before")
    @classmethod
    def from_response(cls, values: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": values["id"],
            "date": datetime.strptime(str(values["date"]), "%Y%m%d").date(),
            "type": values["type"].lower().replace("_", "-"),
            "kcal": values["kcal"],
            "protein": values["protein"],
            "foods": values["foods"],
        }


Meals = TypeAdapter(list[Meal])
