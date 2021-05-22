from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

from django.db.models.fields import CharField
from django.core.validators import MinValueValidator, MaxValueValidator



class User(AbstractUser):
    pass

    def __str__(self):
            return f"{self.first_name} {self.last_name}"

class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category}"

class State(models.Model):
    CC_FIPS = models.CharField(max_length=2)
    CC_ISO = models.CharField(max_length=2)
    STATE_NAME = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.STATE_NAME}"

class Country(models.Model):
    CC_FIPS = models.CharField(max_length=2)
    CC_ISO = models.CharField(max_length=2)
    COUNTRY_NAME = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.COUNTRY_NAME}"

class Map(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    map_data = models.CharField(max_length=100000)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="maps", null=True)
    time_created = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    country_name = models.ForeignKey(Country, on_delete=models.SET_NULL, related_name="maps", null=True)
    state_name = models.ForeignKey(State, on_delete=models.SET_NULL, related_name="maps", null=True)
    starting_location = models.CharField(max_length = 100)
    starting_location_1 = models.DecimalField(max_digits=30, decimal_places=20)
    starting_location_2 = models.DecimalField(max_digits=30, decimal_places=20)
    duration_hours = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)])
    duration_minutes = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(59)])
    distance = models.DecimalField(max_digits=10, decimal_places=3)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="maps", null=True)
    cover = models.ImageField(upload_to='images/', verbose_name='Cover picture:')
    long = models.ImageField(upload_to='images/', verbose_name='Portrait picture:')
    small_1 = models.ImageField(upload_to='images/', verbose_name='A small picture:')
    small_2 = models.ImageField(upload_to='images/', verbose_name='A small picture (one more for good luck):')

    def __str__(self):
        return f"Map: {self.title}."