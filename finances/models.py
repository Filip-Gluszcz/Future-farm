from django.db import models
from account.models import Farm
from production_cycle.models import Cycle
from django.contrib.auth.models import User

# Create your models here.

class CompanyFinance(models.Model):
    total_revenues = models.FloatField(default=0)
    total_expenses = models.FloatField(default=0)
    total_balance = models.FloatField(default=0)
    total_contributions = models.FloatField(default=0)
    total_withdrawal = models.FloatField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class FarmFinance(models.Model):
    total_revenues = models.FloatField(default=0)
    total_expenses = models.FloatField(default=0)
    total_balance = models.FloatField(default=0)
    total_contributions = models.FloatField(default=0)
    total_withdrawal = models.FloatField(default=0)
    farm = models.OneToOneField(Farm, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Transaction(models.Model):
    REVENUE = 'Przychód'
    EXPENSE = 'Wydatek'
    TRANSACTION_TYPES = [
        (REVENUE, 'Przychód'),
        (EXPENSE, 'Wydatek'),
    ]
    FEED = 'Pasza'
    MEDICATION = 'Farmaceutyk'
    HERD = 'Stado'
    SLAUGHTER = 'Ubój'
    OTHER = 'Inne'
    CATEGORIES = [
        (FEED, 'Pasza'),
        (MEDICATION, 'Farmaceutyk'),
        (HERD, 'Stado'),
        (SLAUGHTER, 'Ubój'),
        (OTHER, 'Inne')
    ]
    title = models.CharField(max_length=50)
    worth = models.FloatField(default=0)
    category = models.CharField(max_length=15, choices=CATEGORIES, default=OTHER)
    type = models.CharField(max_length=15, choices=TRANSACTION_TYPES, default=EXPENSE)
    recipient_sender = models.CharField(max_length=50)
    internal = models.BooleanField(default=False)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)


class ToAccount(models.Model):
    title = models.CharField(max_length=50)
    worth = models.FloatField(default=0)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    


