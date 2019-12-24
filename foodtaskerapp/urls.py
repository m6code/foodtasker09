from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('', views.home, name='home'),
	    path('restaurant/sign-in/', auth_views.LoginView.as_view(template_name='foodtaskerapp/restaurant/sign_in.html'),
	  	name='restaurant-sign-in'),
    path('restaurant/sign-out/', auth_views.LogoutView.as_view(next_page='/'),
	  	name='restaurant-sign-out'),
    path('restaurant/', views.restaurant_home, name='restaurant-home'),
    path('restaurant/sign-up/', views.restaurant_sign_up, name='restaurant-sign-up'),
    path('restaurant/account/', views.restaurant_account, name='restaurant-account'),
    path('restaurant/meal/', views.restaurant_meal, name='restaurant-meal'),
    path('restaurant/order/', views.restaurant_order, name='restaurant-order'),
    path('restaurant/report/', views.restaurant_report, name='restaurant-report'),

    path('restaurant/meal/add/', views.restaurant_add_meal, name='restaurant-add-meal'),
    path('restaurant/meal/', views.restaurant_meal, name='restaurant-meal'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)