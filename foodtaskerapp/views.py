from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


from .models import Meal
from .forms import UserForm, RestaurantForm , UserFormEdit, MealForm

def home(request):
	return redirect(restaurant_home)

@login_required(login_url='/restaurant/sign-in/')
def restaurant_home(request):
	# return render(request, 'foodtaskerapp/restaurant/home.html', {})
	return redirect(restaurant_order)


@login_required(login_url='/restaurant/sign-in/')
def restaurant_account(request):
	user_form_edit = UserFormEdit(instance = request.user)
	restaurant_form_edit = RestaurantForm(instance = request.user.restaurant)

	if request.method == "POST":
		user_form_edit = UserFormEdit(request.POST, instance=request.user)
		restaurant_form_edit = RestaurantForm(request.POST, request.FILES, instance = request.user.restaurant)

		if user_form_edit.is_valid() and restaurant_form_edit.is_valid():
			user_form_edit.save()
			restaurant_form_edit.save()

	return render(request, 'foodtaskerapp/restaurant/account.html', {
		"user_form_edit": user_form_edit,
		"restaurant_form_edit": restaurant_form_edit
		})

@login_required(login_url='/restaurant/sign-in/')
def restaurant_meal(request):
	meals = Meal.objects.filter(restaurant = request.user.restaurant).order_by("-id")
	return render(request, 'foodtaskerapp/restaurant/meal.html', {
		"meals": meals
		})

@login_required(login_url='/restaurant/sign-in/')
def restaurant_add_meal(request):
	form = MealForm()

	if request.method == "POST":
		form = MealForm(request.POST, request.FILES)

		if form.is_valid():
			meal = form.save(commit=False)
			meal.restaurant = request.user.restaurant
			meal.save()
			return redirect(restaurant_meal)

	return render(request, 'foodtaskerapp/restaurant/add_meal.html', {
		"form": form,
		})

@login_required(login_url='/restaurant/sign-in/')
def restaurant_edit_meal(request, meal_id):
	form = MealForm(instance = Meal.objects.get(id = meal_id ))

	if request.method == "POST":
		form = MealForm(request.POST, request.FILES, instance = Meal.objects.get(id = meal_id ))

		if form.is_valid():
			form.save()
			return redirect(restaurant_meal)

	return render(request, 'foodtaskerapp/restaurant/edit_meal.html', {
		"form": form,
		})



@login_required(login_url='/restaurant/sign-in/')
def restaurant_order(request):
	return render(request, 'foodtaskerapp/restaurant/order.html', {})

@login_required(login_url='/restaurant/sign-in/')
def restaurant_report(request):
	return render(request, 'foodtaskerapp/restaurant/report.html', {})

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