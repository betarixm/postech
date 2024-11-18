from datetime import date

from pyattendance.client.functions import attend, lecture_list, r002, u001
from pyattendance.client.models import (
    Connection,
    LectureListResponse,
    R002Response,
    U001Response,
    User,
)


def test_lecture_list(connection: Connection, user: User):
    response = lecture_list(connection, user, date.today())
    assert isinstance(response, LectureListResponse)


def test_r002(connection: Connection, user: User):
    response = r002(
        connection,
        user,
        (2024, "2"),
        [],
    )
    assert isinstance(response, R002Response)


def test_u001(connection: Connection, user: User):
    response = u001(
        connection,
        user,
        [],
    )
    assert isinstance(response, U001Response)


def test_attend(connection: Connection, user: User):
    r002_response, u001_response = attend(
        connection,
        user,
        (2024, "2"),
        [],
    )
    assert isinstance(r002_response, R002Response)
    assert isinstance(u001_response, U001Response)
