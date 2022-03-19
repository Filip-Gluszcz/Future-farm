from django.db import models
from account.models import Farm, Profile
from production_cycle.models import Cycle, FeedDelivery, Slaughter, Medication
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete

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
    


@receiver(post_save, sender=Farm)
def auto_create_farm_finance(sender, instance, created, **kwargs):
    if created:
        FarmFinance.objects.create(farm=instance, user=instance.user)


@receiver(post_save, sender=Profile)
def auto_create_company_finance(sender, instance, created, **kwargs):
    if created:
        CompanyFinance.objects.create(user=instance.user)


@receiver(post_save, sender=FeedDelivery)
def auto_create_feed_delivery_to_account(sender, instance, created, **kwargs):
    if created:
        worth = instance.quantity * instance.price
        ToAccount.objects.create(title=f"Pasza {instance.choices} {instance.quantity}t", worth=worth, farm=instance.cycle.farm, cycle=instance.cycle, user=instance.cycle.farm.user)


@receiver(post_save, sender=Cycle)
def auto_create_cycle_herd_to_account(sender, instance, created, **kwargs):
    if created:
        ToAccount.objects.create(title=f"Stado {instance.hybryd} {instance.herd_size}szt.", worth=0, farm=instance.farm, cycle=instance, user=instance.farm.user)


@receiver(post_save, sender=Slaughter)
def auto_create_slaughter_to_account(sender, instance, created, **kwargs):
    if created:
        worth = instance.quantity * instance.price
        ToAccount.objects.create(title=f"Ubój {instance.quantity}szt. {instance.slaughterhouse}", worth=worth, farm=instance.cycle.farm, cycle=instance.cycle, user=instance.cycle.farm.user)


@receiver(post_save, sender=Medication)
def auto_create_medication_to_account(sender, instance, created, **kwargs):
    if created:
        ToAccount.objects.create(title=f"{instance.type} {instance.name}", worth=instance.price, farm=instance.farm, cycle=instance.farm.cycle_set.last(), user=instance.farm.user)


@receiver(pre_save, sender=Transaction)
def transaction_pre_save(sender, instance, **kwargs):
    try:
        instance._pre_save_instance = Transaction.objects.get(pk=instance.pk)
    except Transaction.DoesNotExist:
        instance._pre_save_instance = instance


@receiver(post_save, sender=Transaction)
def update_farm_finance(sender, instance, created, **kwargs):
    farmFinance = FarmFinance.objects.get(farm=instance.farm)
    if created:
        if instance.internal:
            if instance.type == 'Przychód':
                farmFinance.total_contributions += instance.worth
            else:
                farmFinance.total_withdrawal += instance.worth
        else:
            if instance.type == 'Przychód':
                farmFinance.total_revenues += instance.worth
            else:
                farmFinance.total_expenses += instance.worth
    else:
        pre_save_instance = instance._pre_save_instance
        if instance.internal:
            if instance.type == 'Przychód':
                farmFinance.total_contributions -= pre_save_instance.worth
                farmFinance.total_contributions += instance.worth
            else:
                farmFinance.total_withdrawal -= pre_save_instance.worth
                farmFinance.total_withdrawal += instance.worth
        else:
            if instance.type == 'Przychód':
                farmFinance.total_revenues -= pre_save_instance.worth
                farmFinance.total_revenues += instance.worth
            else:
                farmFinance.total_expenses -= pre_save_instance.worth
                farmFinance.total_expenses += instance.worth
    
    farmFinance.total_balance = (farmFinance.total_revenues + farmFinance.total_contributions) - (farmFinance.total_expenses + farmFinance.total_withdrawal)
    farmFinance.save()


@receiver(post_delete, sender=Transaction)
def update_by_deleting_transaction(sender, instance, **kwargs):
    farmFinance = FarmFinance.objects.get(farm=instance.farm)
    if instance.internal:
        if instance.type == 'Przychód':
            farmFinance.total_contributions -= instance.worth
        else:
            farmFinance.total_withdrawal -= instance.worth
    else:
        if instance.type == 'Przychód':
            farmFinance.total_revenues -= instance.worth
        else:
            farmFinance.total_expenses -= instance.worth
    
    farmFinance.total_balance = (farmFinance.total_revenues + farmFinance.total_contributions) - (farmFinance.total_expenses + farmFinance.total_withdrawal)
    farmFinance.save()


@receiver(pre_save, sender=FarmFinance)
def farm_finance_pre_save(sender, instance, **kwargs):
    try:
        instance._pre_save_instance = FarmFinance.objects.get(pk=instance.pk)
    except FarmFinance.DoesNotExist:
        instance._pre_save_instance = instance


@receiver(post_save, sender=FarmFinance)
def company_finance_update(sender, instance, created, **kwargs):
    companyFinance = CompanyFinance.objects.get(user=instance.user)
    if created:
        companyFinance.total_revenues += instance.total_revenues
        companyFinance.total_expenses += instance.total_expenses
        companyFinance.total_contributions += instance.total_contributions
        companyFinance.total_withdrawal += instance.total_withdrawal
    else:
        pre_save_instance = instance._pre_save_instance

        companyFinance.total_revenues -= pre_save_instance.total_revenues
        companyFinance.total_expenses -= pre_save_instance.total_expenses
        companyFinance.total_contributions -= pre_save_instance.total_contributions
        companyFinance.total_withdrawal -= pre_save_instance.total_withdrawal

        companyFinance.total_revenues += instance.total_revenues
        companyFinance.total_expenses += instance.total_expenses
        companyFinance.total_contributions += instance.total_contributions
        companyFinance.total_withdrawal += instance.total_withdrawal

    companyFinance.total_balance = (companyFinance.total_revenues + companyFinance.total_contributions) - (companyFinance.total_expenses + companyFinance.total_withdrawal)
    companyFinance.save()