from django.db import models
from django.utils import dateformat, timezone

from identity.models import User


class Device(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    uuid = models.CharField(max_length=36, primary_key=True, unique=True)
    povis_id = models.CharField(max_length=32)
    app_version = models.CharField(max_length=16)
    locale = models.CharField(max_length=5)
    mac_address = models.CharField(max_length=17)
    type = models.IntegerField()
    version = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.povis_id} ({self.uuid})"


class Connection(models.Model):
    protocol = models.CharField(max_length=16)
    host = models.CharField(max_length=255)
    port = models.IntegerField()

    @property
    def url(self):
        return f"{self.protocol}://{self.host}:{self.port}/"

    class Meta:
        unique_together = ("protocol", "host", "port")

    def __str__(self):
        return self.url


class Lecture(models.Model):
    id = models.CharField(max_length=255, primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=16)
    year = models.IntegerField()
    term = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.name or self.id} ({self.year}, {self.term})"


class Ble(models.Model):
    uuid = models.CharField(max_length=255)
    major = models.IntegerField()
    minor = models.IntegerField()

    class Meta:
        unique_together = ("uuid", "major", "minor")

    def __str__(self):
        return f"{self.uuid} ({self.major}, {self.minor})"


class Session(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    ble = models.ForeignKey(Ble, on_delete=models.PROTECT, null=True)
    session_start = models.DateTimeField()
    session_end = models.DateTimeField()
    attendance_start = models.DateTimeField()
    attendance_end = models.DateTimeField()
    late_start = models.DateTimeField()
    late_end = models.DateTimeField()
    absence_start = models.DateTimeField()
    absence_end = models.DateTimeField()

    def __str__(self):
        return f"{self.lecture} ({self.user}, {dateformat.format(timezone.localtime(self.session_start), "H:i")} - {dateformat.format(timezone.localtime(self.session_end), "H:i")})"

    class Meta:
        unique_together = ("lecture", "user", "session_start", "session_end")
        ordering = ("-session_start",)


class Room(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    building = models.CharField(max_length=255)

    class Meta:
        unique_together = ("name", "building")

    def __str__(self):
        return f"{self.name} ({self.building})"


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    status = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} ({self.session}, {self.status})"
