from datetime import date

from pyattendance.client.functions import attend, lecture_list
from pyattendance.client.models import (
    AttendResponse,
    Connection,
    LectureListResponse,
    User,
)


def test_lecture_list(connection: Connection, user: User):
    response = lecture_list(connection, user, date.today())
    assert isinstance(response, LectureListResponse)


def test_attend(connection: Connection, user: User):
    response = attend(
        connection,
        user,
        (2024, "2"),
        [],
    )
    assert isinstance(response, AttendResponse)
