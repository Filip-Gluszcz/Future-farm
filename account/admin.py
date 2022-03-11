from django.contrib import admin
from .models import Farm, Profile, Silo

# Register your models here.

admin.site.register(Farm)
admin.site.register(Profile)
admin.site.register(Silo)
