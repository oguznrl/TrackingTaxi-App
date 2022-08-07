from django.contrib import admin
from .models import UserLoginTime , UserLogoutTime , UserCourier
admin.site.register([UserLoginTime,UserLogoutTime,UserCourier])
