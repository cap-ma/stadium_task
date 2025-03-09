from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("stadium_owner", 'StadiumOwner'),
        ('client', "Client"),

    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)


class FootballField(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='fields', null=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=100)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
    
class Image(models.Model):
    name = models.CharField(max_length=255)
    path = models.ImageField(upload_to='media/images')
    football_field = models.ForeignKey(FootballField, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.football_field.name}'

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    field = models.ForeignKey(FootballField, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['booking_date']),
            models.Index(fields=['start_time']),
            models.Index(fields=['end_time']),
            models.Index(fields=['field']),
        ]

    def __str__(self):
        return f"{self.field.name}" - {self.booking_date} ({self.start_time}-{self.end_time})
    