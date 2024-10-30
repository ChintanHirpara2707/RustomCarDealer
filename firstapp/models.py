from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class userRegister(models.Model):
    username = models.CharField(max_length=120, unique=True)
    email = models.EmailField(max_length=120, unique=True)
    password = models.CharField(max_length=128)  # Ensure this is large enough
    phone = models.CharField(max_length=10)
    branch = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)

class Car(models.Model):
    car_name = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255)
    car_engine = models.CharField(max_length=100)
    car_power = models.CharField(max_length=100)
    seating_capacity = models.IntegerField()
    transmission = models.CharField(max_length=20)
    car_image = models.ImageField(upload_to='car_images/')

    def __str__(self):
        return self.car_name
    
class Contact(models.Model):
    email = models.EmailField()
    phone_no = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.email    

class ContactMessage(models.Model):
    email = models.EmailField()
    phone_no = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.email
    
class CustomerReview(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    review = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.rating} stars"
    
class TestDrive(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    car_model = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} - {self.car_model}'