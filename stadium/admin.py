from django.contrib import admin
from .models import Booking, User, FootballField, Image

admin.site.register(User)
admin.site.register(Booking)
admin.site.register(FootballField)
admin.site.register(Image)

# Register your models here.
