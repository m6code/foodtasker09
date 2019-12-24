from django.contrib import admin

from .models import Restaurant, Customer, Meal, Driver

admin.site.register(Restaurant)
admin.site.register(Customer)
admin.site.register(Meal)
admin.site.register(Driver)