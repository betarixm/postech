import pytest
from dotenv import dotenv_values

from pyattendance.client.models import Connection, Device, User


@pytest.fixture
def connection():
    return Connection(protocol="https", host="rollbook.postech.ac.kr", port=443)


@pytest.fixture
def user(device: Device):
    student_id = dotenv_values(".env").get("STUDENT_ID", None)

    assert student_id is not None, "STUDENT_ID is not set in .env file"

    return User(device=device, student_id=student_id)


@pytest.fixture
def device():
    uuid = dotenv_values(".env").get("DEVICE_UUID", None)
    povis_id = dotenv_values(".env").get("POVIS_ID", None)

    assert uuid is not None, "DEVICE_UUID is not set in .env file"
    assert povis_id is not None, "POVIS_ID is not set in .env file"

    return Device(
        uuid=uuid,
        povis_id=povis_id,
        app_version="1.1.10",
        locale="ko_KR",
        mac_address="02:00:00:00:00:00",
        type=20,
        version="18.0.1",
    )
