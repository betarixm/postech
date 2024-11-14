from datetime import date, datetime, timedelta

from django.db.models import Q
from django.utils import timezone
from django.utils.timezone import make_aware
from pyattendance.client.functions import attend, lecture_list
from pyattendance.client.models import Connection as _Connection
from pyattendance.client.models import RoomBle as _RoomBle
from pyattendance.client.models import User as _User

from automata.celery import app
from identity.models import User

from .models import Ble, Connection, Device, Lecture, Log, Room, Session


@app.task
def register_sessions_of_users():
    users = User.objects.all()

    for user in users:
        _register_sessions_of_user.delay(user)


@app.task(max_retries=10)
def _register_sessions_of_user(user: User):
    device = Device.objects.get(user=user)

    # TODO: Logic to get the available connection
    connection = Connection.objects.first()
    assert connection is not None

    response = lecture_list(
        connection=_pyattendance_connection(connection),
        user=_pyattendance_user(user, device),
        current_date=date.today(),
    )

    year, term = response.body.term

    for _pyattendance_lecture in response.body.lectures:
        lecture, _ = Lecture.objects.get_or_create(
            id=_pyattendance_lecture.id, defaults={"year": year, "term": term}
        )

        session_start = make_aware(
            datetime.combine(
                _pyattendance_lecture.date,
                _pyattendance_lecture.periods[0].start,
            ),
            _pyattendance_lecture.periods[0].start.tzinfo,
        )

        session_end = make_aware(
            datetime.combine(
                _pyattendance_lecture.date,
                _pyattendance_lecture.periods[0].end,
            ),
            _pyattendance_lecture.periods[0].end.tzinfo,
        )

        attendance_start = session_start - timedelta(
            minutes=_pyattendance_lecture.attend_start_offset
        )

        attendance_end = session_start

        late_start = session_start + timedelta(
            minutes=_pyattendance_lecture.late_start_offset
        )
        late_end = session_start + timedelta(
            minutes=_pyattendance_lecture.absence_start_offset
        )

        absence_start = late_end
        absence_end = session_end

        ble, _ = Ble.objects.get_or_create(
            uuid=_pyattendance_lecture.room_bles[0].uuid,
            major=_pyattendance_lecture.room_bles[0].major,
            minor=_pyattendance_lecture.room_bles[0].minor,
        )

        Session.objects.get_or_create(
            lecture=lecture,
            user=user,
            defaults={
                "session_start": session_start,
                "session_end": session_end,
                "attendance_start": attendance_start,
                "attendance_end": attendance_end,
                "late_start": late_start,
                "late_end": late_end,
                "absence_start": absence_start,
                "absence_end": absence_end,
                "ble": ble,
            },
        )


@app.task
def attend_sessions():
    now = timezone.now()

    sessions = (
        Session.objects.filter(attendance_start__lte=now, attendance_end__gte=now)
        .filter(Q(log__status__isnull=True) | ~Q(log__status="출석"))
        .distinct()
        .all()
    )

    for session in sessions:
        _attend_session.delay(session)


@app.task(max_retries=3)
def _attend_session(session: Session):
    # TODO: Logic to get the available connection
    connection = Connection.objects.first()
    assert connection is not None, "Connection is not set for the session"

    assert session.ble is not None, "BLE is not set for the session"

    response = attend(
        connection=_pyattendance_connection(connection),
        user=_pyattendance_user(session.user, Device.objects.get(user=session.user)),
        room_bles=[_pyattendance_room_ble(session.ble)],
        term=(session.lecture.year, session.lecture.term),
    )

    Room.objects.get_or_create(
        name=response.body.room, building=response.body.building, session=session
    )

    Log.objects.create(
        user=session.user, session=session, status=response.body.attend_status
    )


def _pyattendance_user(user: User, device: Device) -> _User:
    return _User.model_validate(
        {
            **user.__dict__,
            "device": device.__dict__,
        }
    )


def _pyattendance_connection(connection: Connection) -> _Connection:
    return _Connection.model_validate(connection.__dict__)


def _pyattendance_room_ble(ble: Ble) -> _RoomBle:
    return _RoomBle.model_validate(
        {"bleUuid": ble.uuid, "bleMajor": ble.major, "bleMinor": ble.minor}
    )
