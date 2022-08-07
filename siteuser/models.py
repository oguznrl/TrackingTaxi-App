from statistics import mode
from tkinter import CASCADE
from xml.parsers.expat import model
from django.conf import settings
from django.db import models
from django.utils import timezone
 
# Create your models here.
class UserLoginTime(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    login_date=models.DateTimeField(
            blank=True, null=True)
    logout_date=models.DateTimeField(
            blank=True, null=True)

class UserLogoutTime(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    logout_date=models.DateTimeField(
            blank=True, null=True)

class UserCourier(models.Model):
        user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        vehicle_id=models.IntegerField(blank=True,null=True)
        lat=models.FloatField(blank=True,null=True)
        lng=models.FloatField(blank=True,null=True)
        last_time=models.DateTimeField(blank=True, null=True)
