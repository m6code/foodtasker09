from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .forms import UserForm, RestaurantForm 

def home(request):
	return redirect(restaurant_home)

@login_required(login_url='/restaurant/sign-in/')
def restaurant_home(request):
	return render(request, 'foodtaskerapp/restaurant/home.html', {})

def restaurant_sign_up(request):
	user_form = UserForm()
	restaurant_form = RestaurantForm()

	if request.method == "POST":
		user_form = UserForm(request.POST)
		restaurant_form = RestaurantForm(request.POST, request.FILES)

		if user_form.is_valid() and restaurant_form.is_valid():
			new_user = User.objects.create_user(**user_form.cleaned_data)
			new_restaurant = restaurant_form.save(commit=False) # create restaurant object in memory without saving to db
			new_restaurant.user = new_user
			new_restaurant.save() # now save to database

			# sign in the just created user
			login(request, authenticate(
				username = user_form.cleaned_data["username"],
				password = user_form.cleaned_data["password"]
				))

			return redirect(restaurant_home) # redirect to the home page after authenticating user

	return render(request, 'foodtaskerapp/restaurant/sign_up.html', {
		"user_form": user_form,
		"restaurant_form": restaurant_form
		})