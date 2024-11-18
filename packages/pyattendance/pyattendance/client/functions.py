from datetime import date

import requests

from pyattendance.client.models import (
    Connection,
    LectureListRequest,
    LectureListResponse,
    R002Request,
    R002Response,
    RoomBle,
    U001Request,
    U001Response,
    User,
)


def lecture_list(connection: Connection, user: User, current_date: date):
    response = requests.post(
        f"{connection.url}/eaas/R013",
        headers={"User-Agent": "Mozilla/4.0 (compatible;)"},
        json=LectureListRequest.as_request_body(
            user, current_date=current_date
        ).model_dump(by_alias=True),
    )

    response.raise_for_status()

    return LectureListResponse.model_validate_json(response.text)


def attend(
    connection: Connection, user: User, term: tuple[int, str], room_bles: list[RoomBle]
):
    return r002(connection, user, term, room_bles), u001(connection, user, room_bles)


def r002(
    connection: Connection, user: User, term: tuple[int, str], room_bles: list[RoomBle]
):
    response = requests.post(
        f"{connection.url}/eaas/R002",
        headers={"User-Agent": "Mozilla/4.0 (compatible;)"},
        json=R002Request.as_request_body(user, term, room_bles).model_dump(
            by_alias=True
        ),
    )

    response.raise_for_status()

    return R002Response.model_validate_json(response.text)


def u001(connection: Connection, user: User, room_bles: list[RoomBle]):
    response = requests.post(
        f"{connection.url}/eaas/U001",
        headers={"User-Agent": "Mozilla/4.0 (compatible;)"},
        json=U001Request.as_request_body(user, room_bles).model_dump(by_alias=True),
    )

    response.raise_for_status()

    return U001Response.model_validate_json(response.text)
