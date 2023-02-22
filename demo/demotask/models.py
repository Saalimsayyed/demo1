from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.mobile


class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_name = models.CharField(max_length=10)
    is_accepted = models.BooleanField()
    date_time = models.DateTimeField(auto_now_add=True)