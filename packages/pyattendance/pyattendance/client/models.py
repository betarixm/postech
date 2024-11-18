from __future__ import annotations

import json
import random
from datetime import date, datetime, time
from typing import Any, Literal

import pytz
from pydantic import BaseModel, ConfigDict, field_serializer, model_validator
from pydantic.alias_generators import to_camel

_server_timezone = pytz.timezone("Asia/Seoul")


class Connection(BaseModel):
    protocol: Literal["http", "https"]
    host: str
    port: int

    @property
    def url(self):
        return f"{self.protocol}://{self.host}:{self.port}"


class RequestHeader(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    device_uuid: str
    login_id: str
    app_ver: str
    device_locale: str
    device_mac: str
    device_type: str
    device_ver: str
    tr_id: str
    tr_ver: str = "3"

    @staticmethod
    def as_request_body(user: User, endpoint_id: str):
        assert user.device is not None

        return RequestHeader(
            device_uuid=user.device.uuid,
            login_id=user.device.povis_id,
            app_ver=user.device.app_version,
            device_locale=user.device.locale,
            device_mac=user.device.mac_address,
            device_type=str(user.device.type),
            device_ver=user.device.version,
            tr_id=endpoint_id,
        )


class ResponseHeader(BaseModel):
    tr_version: int
    tr_id: str
    system_time: datetime
    sso_token: Literal[""] | str
    response_code: str
    response_message: str

    @property
    def success(self):
        return self.response_message == "성공"

    @model_validator(mode="before")
    @classmethod
    def from_response(cls, values: dict[str, Any]) -> dict[str, Any]:
        return {
            "tr_version": int(values["trVer"]),
            "tr_id": values["trId"],
            "system_time": datetime.strptime(values["sysTime"], "%Y%m%d%H%M%S").replace(
                tzinfo=_server_timezone
            ),
            "sso_token": values["ssoToken"],
            "response_code": values["resCd"],
            "response_message": values["resMsg"],
        }


class LectureListRequestBody(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    user_id: str
    current_date: str  # YYYYMMDD

    @staticmethod
    def as_request_body(user: User, current_date: date):
        return LectureListRequestBody(
            user_id=user.student_id,
            current_date=current_date.strftime(r"%Y%m%d"),
        )


class LectureListRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    header: RequestHeader
    body: LectureListRequestBody

    @staticmethod
    def as_request_body(user: User, current_date: date):
        return LectureListRequest(
            header=RequestHeader.as_request_body(
                user,
                endpoint_id="R013",
            ),
            body=LectureListRequestBody.as_request_body(
                user, current_date=current_date
            ),
        )


class Period(BaseModel):
    start: time
    end: time

    @model_validator(mode="before")
    @classmethod
    def from_response(cls, values: dict[str, Any]) -> dict[str, Any]:
        return {
            "start": datetime.strptime(values["startTime"], "%H%M")
            .replace(tzinfo=_server_timezone)
            .time(),
            "end": datetime.strptime(values["endTime"], "%H%M")
            .replace(tzinfo=_server_timezone)
            .time(),
        }


class RoomBle(BaseModel):
    uuid: str
    major: int
    minor: int

    @model_validator(mode="before")
    @classmethod
    def from_response(cls, values: dict[str, Any]) -> dict[str, Any]:
        return {
            "uuid": values["bleUuid"],
            "major": int(values["bleMajor"]),
            "minor": int(values["bleMinor"]),
        }


class Lecture(BaseModel):
    id: str
    date: date
    attend_start_offset: int
    late_start_offset: int
    absence_start_offset: int
    class_sort: int
    periods: list[Period]
    room_bles: list[RoomBle]

    @model_validator(mode="before")
    @classmethod
    def from_response(cls, values: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": values["lectureId"],
            "date": datetime.strptime(values["day"], "%Y%m%d")
            .replace(tzinfo=_server_timezone)
            .date(),
            "attend_start_offset": int(values["attendStartTime"]),
            "late_start_offset": int(values["lateStartTime"]),
            "absence_start_offset": int(values["absenceStartTime"]),
            "class_sort": int(values["classSort"]),
            "periods": values["periodList"],
            "room_bles": values["roomBleList"],
        }


class LectureListResponseBody(BaseModel):
    term: tuple[int, str]
    term_start: date
    term_end: date
    next_day_start: date
    lectures: list[Lecture]

    @model_validator(mode="before")
    @classmethod
    def from_response(cls, values: dict[str, Any]) -> dict[str, Any]:
        return {
            "term": (int(values["yearTerm"][:4]), values["yearTerm"][4:]),
            "term_start": datetime.strptime(values["yearTermStart"], "%Y%m%d")
            .replace(tzinfo=_server_timezone)
            .date(),
            "term_end": datetime.strptime(values["yearTermEnd"], "%Y%m%d")
            .replace(tzinfo=_server_timezone)
            .date(),
            "next_day_start": datetime.strptime(values["nextDayStart"], "%Y%m%d")
            .replace(tzinfo=_server_timezone)
            .date(),
            "lectures": values["lectureList"],
        }


class LectureListResponse(BaseModel):
    header: ResponseHeader
    body: LectureListResponseBody

    @model_validator(mode="before")
    @classmethod
    def from_response(cls, values: dict[str, Any]) -> dict[str, Any]:
        match values["body"]:
            case "":
                header = ResponseHeader.model_validate(json.loads(values["header"]))
                raise ValueError(header.response_message)
            case _:
                return {
                    "header": json.loads(values["header"]),
                    "body": json.loads(values["body"]),
                }


class R002RequestBody(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    user_id: str
    year_term: str
    ble_list: list[RoomBle]

    @staticmethod
    def as_request_body(user: User, term: tuple[int, str], room_bles: list[RoomBle]):
        return R002RequestBody(
            user_id=user.device.povis_id,
            year_term=f"{term[0]}{term[1]}",
            ble_list=room_bles,
        )

    @field_serializer("ble_list")
    def _serialize_ble_list(self, values: list[RoomBle]) -> list[dict[str, Any]]:
        return [
            {
                **value.model_dump(by_alias=True),
                "bleRssi": str(random.randint(-80, -60)),
            }
            for value in values
        ]


class R002Request(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    header: RequestHeader
    body: R002RequestBody

    @staticmethod
    def as_request_body(user: User, term: tuple[int, str], room_bles: list[RoomBle]):
        return R002Request(
            header=RequestHeader.as_request_body(user, endpoint_id="R002"),
            body=R002RequestBody.as_request_body(user, term=term, room_bles=room_bles),
        )


class R002ResponseBody(BaseModel):
    room: str
    building: str
    date: date
    lecture_id: str
    term: tuple[int, str]
    attend_status: str

    @model_validator(mode="before")
    @classmethod
    def from_response(cls, values: dict[str, Any]) -> dict[str, Any]:
        return {
            "room": values["bleRoomNm"],
            "building": values["bleBuildingNm"],
            "date": datetime.strptime(values["day"], "%Y%m%d")
            .replace(tzinfo=_server_timezone)
            .date(),
            "lecture_id": values["lectureId"],
            "term": (int(values["term"][:4]), values["term"][4:]),
            "attend_status": values["attendStatus"],
        }


class R002Response(BaseModel):
    header: ResponseHeader
    body: R002ResponseBody

    @model_validator(mode="before")
    @classmethod
    def from_response(cls, values: dict[str, Any]) -> dict[str, Any]:
        match values["body"]:
            case "":
                header = ResponseHeader.model_validate(json.loads(values["header"]))
                raise ValueError(header.response_message)
            case _:
                return {
                    "header": json.loads(values["header"]),
                    "body": json.loads(values["body"]),
                }


class U001RequestBody(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    ble_list: list[RoomBle]

    @staticmethod
    def as_request_body(room_bles: list[RoomBle]):
        return U001RequestBody(ble_list=room_bles)

    @field_serializer("ble_list")
    def _serialize_ble_list(self, values: list[RoomBle]) -> list[dict[str, Any]]:
        return [
            {
                **value.model_dump(by_alias=True),
                "bleRssi": str(random.randint(-80, -60)),
            }
            for value in values
        ]


class U001Request(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    header: RequestHeader
    body: U001RequestBody

    @staticmethod
    def as_request_body(user: User, room_bles: list[RoomBle]):
        return U001Request(
            header=RequestHeader.as_request_body(user, endpoint_id="U001"),
            body=U001RequestBody.as_request_body(room_bles=room_bles),
        )


class U001Response(BaseModel):
    header: ResponseHeader

    @model_validator(mode="before")
    @classmethod
    def from_response(cls, values: dict[str, Any]) -> dict[str, Any]:
        return {
            "header": json.loads(values["header"]),
        }


class Device(BaseModel):
    uuid: str
    povis_id: str
    app_version: str
    locale: str
    mac_address: str
    type: int
    version: str


class User(BaseModel):
    device: Device
    student_id: str
