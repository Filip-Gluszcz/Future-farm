from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    nip = models.IntegerField()
    regon = models.IntegerField()
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    number = models.CharField(max_length=30)
    postal_code = models.IntegerField(default=0)

class Farm(models.Model):
    name = models.CharField(max_length=50)
    max_herd_size = models.IntegerField(default=0)
    surface = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return str(self.name)

class Silo(models.Model):
    STARTER = 'Starter'
    GROWER = 'Grower'
    FINISHER = 'Finisher'
    FEED_CHOICES = [
        (STARTER, 'Starter'),
        (GROWER, 'Grower'),
        (FINISHER, 'Finisher')
    ]
    number = models.IntegerField(default=0)
    capacity = models.FloatField(default=0)
    feet_type = models.CharField(max_length=15, choices=FEED_CHOICES, default=STARTER)
    state = models.FloatField(default=0)
    farm = models.ForeignKey(Farm, on_delete=CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return 'Silos ' + str(self.number)

