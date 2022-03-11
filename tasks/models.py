from django.db import models
from django.db.models.deletion import CASCADE
from account.models import Farm
from django.contrib.auth.models import User


class Task(models.Model):
    NEW = 'NEW'
    DURING = 'DURING'
    DONE = 'DONE'
    STATUS_CHOICES = [
        (NEW, 'New'),
        (DURING, 'During'),
        (DONE, 'Done')
    ]
    date = models.DateField(auto_now=True)
    text = models.CharField(max_length=100)
    important = models.BooleanField(default=False)
    status = models.CharField(
        max_length=6, choices=STATUS_CHOICES, default=NEW)
    farm = models.ForeignKey(Farm, on_delete=CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=CASCADE, null=True)

    def __str__(self):
        return str(self.text)
 