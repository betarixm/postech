from django.contrib import admin

from .models import Ble, Connection, Device, Lecture, Log, Room, Session

admin.site.register(Ble)
admin.site.register(Connection)
admin.site.register(Device)
admin.site.register(Lecture)
admin.site.register(Log)
admin.site.register(Room)
admin.site.register(Session)
