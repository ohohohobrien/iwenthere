from django.contrib import admin
from .models import User, Map, Category, State, Country

# Register your models here.

admin.site.register(User)
admin.site.register(Map)
admin.site.register(Category)
admin.site.register(State)
admin.site.register(Country)