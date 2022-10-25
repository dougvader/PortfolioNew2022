# This file forms part of the Smart-City Project 
# IFB299 S2-2017 Group 68 
# Description: This file represents system entities and variables

from django.db import models
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser

# User Entity 
class User(AbstractUser):
    user_type = models.CharField(max_length=250)

# Mall Entity
class Mall(models.Model):
    mall_ID = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    image_url = models.CharField(max_length=500)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    def __str__(self):  #For Python 2, use __str__ on Python 3
        return self.name
	
# Hotel Entity 
class Hotel(models.Model):
    hotel_ID = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    image_url = models.CharField(max_length=500)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    def __str__(self):  #For Python 2, use __str__ on Python 3
        return self.name
	
# Park Entity 
class Park(models.Model):
    park_ID = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    image_url = models.CharField(max_length=500)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    def __str__(self):  #For Python 2, use __str__ on Python 3
        return self.name
    
# College Entity 
class College(models.Model):
    college_ID = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    department = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    image_url = models.CharField(max_length=500)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    def __str__(self):  #For Python 2, use __str__ on Python 3
        return self.name
    
# Library Entity 
class Library(models.Model):
    library_ID = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    image_url = models.CharField(max_length=500)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    def __str__(self):  #For Python 2, use __str__ on Python 3
        return self.name
    
# Zoo Entity 
class Zoo(models.Model):
    zoo_ID = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    image_url = models.CharField(max_length=500)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    def __str__(self):  #For Python 2, use __str__ on Python 3
        return self.name
    
# Museum Entity 
class Museum(models.Model):
    museum_ID = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    image_url = models.CharField(max_length=500)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    def __str__(self):  #For Python 2, use __str__ on Python 3
        return self.name
    
# Industry Entity 
class Industry(models.Model):
    industry_ID = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    image_url = models.CharField(max_length=500)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    def __str__(self):  #For Python 2, use __str__ on Python 3
        return self.name
    
# Restaurant Entity 
class Restaurant(models.Model):
    restaurant_ID = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    image_url = models.CharField(max_length=500)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    def __str__(self):  #For Python 2, use __str__ on Python 3
        return self.name
    
# City Entity 
class City(models.Model):
    city_ID = models.CharField(max_length=500)
    Name = models.CharField(max_length=500)
    Service = models.CharField(max_length=500)
    
    def __str__(self):  #For Python 2, use __str__ on Python 3
        return self.Name
	
class Mall_Favourites(models.Model):
	user = models.ForeignKey(User, unique=False)
	mall = models.ForeignKey(Mall, unique =False)
	
class Hotel_Favourites(models.Model):
	user = models.ForeignKey(User, unique=False)
	hotel = models.ForeignKey(Hotel, unique =False)
	
class Park_Favourites(models.Model):
	user = models.ForeignKey(User, unique=False)
	park = models.ForeignKey(Park, unique =False)
	
class College_Favourites(models.Model):
	user = models.ForeignKey(User, unique=False)
	college = models.ForeignKey(College, unique =False)
	
class Library_Favourites(models.Model):
	user = models.ForeignKey(User, unique=False)
	library = models.ForeignKey(Library, unique =False)
	
class Zoo_Favourites(models.Model):
	user = models.ForeignKey(User, unique=False)
	zoo = models.ForeignKey(Zoo, unique =False)
	
class Museum_Favourites(models.Model):
	user = models.ForeignKey(User, unique=False)
	museum = models.ForeignKey(Museum, unique =False)

class Industry_Favourites(models.Model):
	user = models.ForeignKey(User, unique=False)
	industry = models.ForeignKey(Industry, unique =False)

class Restaurant_Favourites(models.Model):
	user = models.ForeignKey(User, unique=False)
	restaurant = models.ForeignKey(Restaurant, unique =False)

class Review_College(models.Model):
    possible_ratings = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),)
    user = models.ForeignKey(User, unique=False)
    college = models.ForeignKey(College, unique =False)
    user_name = models.CharField(max_length=500)
    comment = models.CharField(max_length=1000)
    rating = models.IntegerField(choices=possible_ratings)

class Review_Library(models.Model):
    possible_ratings = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),)
    user = models.ForeignKey(User, unique=False)
    library = models.ForeignKey(Library, unique =False)
    user_name = models.CharField(max_length=500)
    comment = models.CharField(max_length=1000)
    rating = models.IntegerField(choices=possible_ratings)

class Review_Industry(models.Model):
    possible_ratings = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),)
    user = models.ForeignKey(User, unique=False)
    industry = models.ForeignKey(Industry, unique =False)
    user_name = models.CharField(max_length=500)
    comment = models.CharField(max_length=1000)
    rating = models.IntegerField(choices=possible_ratings)

class Review_Hotel(models.Model):
    possible_ratings = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),)
    user = models.ForeignKey(User, unique=False)
    hotel = models.ForeignKey(Hotel, unique =False)
    user_name = models.CharField(max_length=500)
    comment = models.CharField(max_length=1000)
    rating = models.IntegerField(choices=possible_ratings)

class Review_Park(models.Model):
    possible_ratings = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),)
    user = models.ForeignKey(User, unique=False)
    park = models.ForeignKey(Park, unique =False)
    user_name = models.CharField(max_length=500)
    comment = models.CharField(max_length=1000)
    rating = models.IntegerField(choices=possible_ratings)

class Review_Zoo(models.Model):
    possible_ratings = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),)
    user = models.ForeignKey(User, unique=False)
    zoo = models.ForeignKey(Zoo, unique =False)
    user_name = models.CharField(max_length=500)
    comment = models.CharField(max_length=1000)
    rating = models.IntegerField(choices=possible_ratings)

class Review_Museum(models.Model):
    possible_ratings = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),)
    user = models.ForeignKey(User, unique=False)
    museum = models.ForeignKey(Museum, unique =False)
    user_name = models.CharField(max_length=500)
    comment = models.CharField(max_length=1000)
    rating = models.IntegerField(choices=possible_ratings)

class Review_Restaurant(models.Model):
    possible_ratings = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),)
    user = models.ForeignKey(User, unique=False)
    restaurant = models.ForeignKey(Restaurant, unique =False)
    user_name = models.CharField(max_length=500)
    comment = models.CharField(max_length=1000)
    rating = models.IntegerField(choices=possible_ratings)

class Review_Mall(models.Model):
    possible_ratings = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),)
    user = models.ForeignKey(User, unique=False)
    mall = models.ForeignKey(Mall, unique =False)
    user_name = models.CharField(max_length=500)
    comment = models.CharField(max_length=1000)
    rating = models.IntegerField(choices=possible_ratings)