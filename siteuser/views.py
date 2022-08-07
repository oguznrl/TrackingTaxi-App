from email.policy import HTTP
import mimetypes
from random import random
import pymongo
from .forms import sortbyDateForm
from django.http import HttpResponseRedirect

from django.http import HttpResponse, JsonResponse
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from .models import UserCourier, UserLogoutTime , UserLoginTime
from django.utils import timezone
from django.http import HttpResponse
from random import seed
from random import random
import json
from datetime import datetime
exist_user=None

myclient = pymongo.MongoClient("mongodb+srv://tanalperen8:oNNcmdOBMJYBk48l@yazlab21.0mqdb.mongodb.net/cars?retryWrites=true&w=majority")
mydb = myclient["cars"]
mycol = mydb["carsCollection2"]
counter = 0

def homepage(request):
    return render(request=request, template_name="siteuser/header.html")

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			user_logi=UserLoginTime()
			user_logi.user=user
			user_logi.login_date=timezone.now()
			user_logi.save()
			global exist_user 
			exist_user=user
			login(request, request.user.id)
			messages.success(request, "Registration successful." )
			return redirect("main:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="siteuser/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				user_logi=UserLoginTime()
				user_logi.user=user
				user_logi.login_date=timezone.now()
				user_logi.save()
				#global exist_user 
				#exist_user=user
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="siteuser/login.html", context={"login_form":form})

def logout_request(request):
	#global exist_user 
	user_logo=UserLoginTime.objects.filter(user=request.user).last()
	user_logo.user=request.user
	user_logo.logout_date=timezone.now()
	user_logo.save()
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/")

def getrandom(request):
	#kullaniciya ait araba ID'lerini alip veri tabaninda o araclara ait verileri ceker ve json seklinde yollar
	list = []
	car_data = dict()
	vehicleIDs = UserCourier.objects.filter(user=request.user)
	for i in vehicleIDs:
		id=str(i.vehicle_id)
		myquery = {"vehicleID": id}
		data = mycol.find(myquery, {'_id': False})
		for x in data:
			list.append(x.copy())
	car_data["data"]=list

	return JsonResponse(car_data,status=200)
def show_map(request):
	ran=random()
	return render(request=request,template_name='siteuser/googlemap.html',context={"x":ran})

def show_data(request):
	data=UserCourier.objects.filter(user=request.user)
	return render(request=request,template_name='siteuser/car_data.html',context={'car':data})

def show_detail(request,id):
	#kullanici sahip oldugu araclardan birine tiklarsa o araca ait default olarak son 30 dklik veri gostermesi
	#icin veri yollar
	myquery = {"vehicleID": str(id)}
	data = mycol.find(myquery)
	dictlist = []
	for x in data:
		date = datetime.strptime((x['date']), '%Y-%m-%d %H:%M')
		now = datetime.now()
		#karsilastirma yapabilmek icin simdiki zamani 2018-11'e ayarlar
		changednow = now.replace(year=2018, month=11)
		if (0 < ((changednow - date).total_seconds()) < 1800):
			dictlist.append(x.copy())

	return render(request=request, template_name='siteuser/car_detail.html', context={'car': dictlist, 'id':id})

def getSortData(request,id):
	#kullanici belirli tarih araligindaki verileri gormek isterse girilen inputa gore duzenleme yaparak
	#verileri cekip yollar
	myquery = {"vehicleID": str(id)}
	data = mycol.find(myquery)
	listt2 = []
	if request.method == 'POST':
		form = sortbyDateForm(request.POST)
		if form.is_valid():
			firstDate = form.cleaned_data.get('firstDate')
			secondDate = form.cleaned_data.get('secondDate')
			inputdate = datetime.strptime((firstDate), '%Y-%m-%d %H:%M')
			inputdate2 = datetime.strptime((secondDate), '%Y-%m-%d %H:%M')
			for x in data:
				date = datetime.strptime((x['date']), '%Y-%m-%d %H:%M')
				if ((inputdate <= date <= inputdate2) or (inputdate2 <= date <= inputdate)):
					listt2.append(x.copy())

	return render(request, 'siteuser/sorted_data.html', {'carr': listt2})

def user_value(request):
	log_data=UserLoginTime.objects.filter(user=request.user)
	return render(request=request,template_name="siteuser/user_data.html",context={'log_user':log_data})
