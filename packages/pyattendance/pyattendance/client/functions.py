from datetime import date

import requests

from pyattendance.client.models import (
    AttendRequest,
    AttendResponse,
    Connection,
    LectureListRequest,
    LectureListResponse,
    RoomBle,
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
    response = requests.post(
        f"{connection.url}/eaas/R002",
        headers={"User-Agent": "Mozilla/4.0 (compatible;)"},
        json=AttendRequest.as_request_body(user, term, room_bles).model_dump(
            by_alias=True
        ),
    )

    response.raise_for_status()

    return AttendResponse.model_validate_json(response.text)
