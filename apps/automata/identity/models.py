from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    student_id = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
