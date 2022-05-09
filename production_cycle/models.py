import os
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from account.models import Farm, Silo
from django.contrib.auth.models import User




class Cycle(models.Model):
    date_of_insertion = models.DateTimeField(auto_now=True)
    hybryd = models.CharField(max_length=30, default="hybryd")
    herd_size = models.IntegerField(default=0)
    chick_avarage_weight = models.FloatField(default=0)
    age_of_the_reproductive_stock = models.CharField(
        max_length=30, default="age")
    hatchery = models.CharField(max_length=30, default="hatchery")
    current_herd_size = models.IntegerField(default=0)
    farm = models.ForeignKey(Farm, on_delete=CASCADE)
    water_meter_value = models.FloatField(default=0)
    
    ACTIVE = 'ACTIVE'
    CLOSED = 'CLOSED'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (CLOSED, 'Closed')
    ]
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default=ACTIVE)

    def __str__(self):
        return 'Cykl ID: ' + str(self.id)



class Day(models.Model):
    date = models.DateTimeField(auto_now=True)
    cycle_day = models.IntegerField(default=0)
    deads = models.IntegerField(default=0)
    selection = models.IntegerField(default=0)
    daily_mortality_rate = models.FloatField(default=0)
    feed_consumption = models.FloatField(default=0)
    daily_wather_consumption = models.FloatField(default=0)
    average_body_weight = models.FloatField(default=0)
    temperature = models.FloatField(default=0)
    humidity = models.FloatField(default=0)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    eww = models.FloatField(default=0)
    fcr = models.FloatField(default=0)
    total_feed = models.FloatField(default=0)
    total_water = models.FloatField(default=0)
    water_meter_value = models.FloatField(default=0)
    increasing_feed_consumption = models.FloatField(default=0)
    total_increasing_feed_consumption = models.FloatField(default=0)

    
    def save(self, *args, **kwargs):
        cycle = self.cycle
        deads = self.deads
        selection = self.selection
        herd_size = cycle.current_herd_size - (deads + selection)
        if herd_size > 0:
            daily_mortality_rate = ((deads + selection) / herd_size) * 100
        else:
            daily_mortality_rate = 0
        self.daily_mortality_rate = round(daily_mortality_rate, 4)
        if self.cycle_day > 0:
            previousDay = Day.objects.get(cycle_day=self.cycle_day-1, cycle=cycle)
            if previousDay.cycle_day == self.cycle_day:
                previousDay = Day.objects.filter(cycle=cycle).order_by('-cycle_day')[1]
            
            water_meter_value = self.water_meter_value
            total_water = water_meter_value - previousDay.water_meter_value
            self.total_water = total_water

            if herd_size > 0:
                daily_wather_consumption = (total_water / herd_size) * 1000
            else:
                daily_wather_consumption = 0
            self.daily_wather_consumption = round(daily_wather_consumption, 1)

            day_standard = Standard.objects.get(cycle_day=self.cycle_day)
            feed_consumption = (day_standard.feed_consumption / day_standard.water_consumption) * daily_wather_consumption
            self.feed_consumption = round(feed_consumption, 1)

            self.total_feed = (feed_consumption * herd_size) / 1000

            increasing_feed_consumption = previousDay.increasing_feed_consumption + feed_consumption
            self.increasing_feed_consumption = increasing_feed_consumption

            total_increasing_feed_consumption = previousDay.total_increasing_feed_consumption + self.total_feed
            self.total_increasing_feed_consumption = total_increasing_feed_consumption

            fcr = increasing_feed_consumption / self.average_body_weight
            self.fcr = round(fcr, 4)

            if (self.cycle_day * fcr) > 0:
                eww = ((((herd_size / self.cycle.herd_size) * 100) * (self.average_body_weight / 1000)) / (self.cycle_day * fcr)) * 100
                self.eww = round(eww)

        super().save(*args, **kwargs)
    
    def __str__(self):
        return 'Cykl id ' + str(self.cycle.id) + ' dzień ' + str(self.cycle_day)

    class Meta:
        ordering = ('cycle_day',)



class CycleCompleted(models.Model):
    cycle = models.OneToOneField(Cycle, on_delete=models.CASCADE)
    total_weight = models.FloatField(default=1)
    number_of_units_sold = models.IntegerField(default=1)
    average_weight = models.FloatField(default=1)
    total_feed = models.FloatField(default=1)
    survival_rate = models.FloatField(default=1)
    total_days = models.IntegerField(default=1)
    fcr = models.FloatField(default=1)
    eww = models.FloatField(default=1)
    total_revenues = models.FloatField(default=0)
    total_expenses = models.FloatField(default=0)
    total_balance = models.FloatField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, **kwargs):
        self.fcr = self.total_feed / self.total_weight
        self.eww = (self.survival_rate * self.average_weight) / (self.total_days * self.fcr)*100
        self.total_revenues = 0
        cycle_revenues = self.cycle.transaction_set.filter(type='Przychód')
        for transaction in cycle_revenues:
            self.total_revenues += transaction.worth

        self.total_expenses = 0
        cycle_expenses = self.cycle.transaction_set.filter(type='Wydatek')
        for transaction in cycle_expenses:
            self.total_expenses += transaction.worth

        self.total_balance = self.total_revenues - self.total_expenses
        
        super().save(**kwargs)

    def __str__(self):
        return 'Rozliczenie cyklu ID: ' + str(self.cycle.id)



class Slaughter(models.Model):
    date = models.DateTimeField(auto_now=True)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    day_id = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    weight = models.FloatField(default=0)
    average_weight = models.FloatField(default=0)
    slaughterhouse = models.CharField(max_length=50)
    price = models.FloatField(default=1)

    def save(self, *args, **kwargs):
        self.average_weight = (self.weight / self.quantity) * 1000
        return super().save()


class FeedDelivery(models.Model):
    STARTER = 'Starter'
    GROWER = 'Grower'
    FINISHER = 'Finisher'
    FEED_CHOICES = [
        (STARTER, 'Starter'),
        (GROWER, 'Grower'),
        (FINISHER, 'Finisher')
    ]
    date = models.DateTimeField(auto_now=True)
    choices = models.CharField(
        max_length=15, choices=FEED_CHOICES, default=STARTER)
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=1)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    silo = models.ForeignKey(Silo, on_delete=CASCADE)


class Medication(models.Model):
    DRUG = 'Lek'
    SUPPLEMENT = 'Suplement'
    VACCINE = 'Szczepienie'
    SOLID = 'Stały'
    LIQUID = 'Płynny'
    MEDICATION_TYPES = [
        (DRUG, 'Lek'),
        (SUPPLEMENT, 'Suplement'),
        (VACCINE, 'Szczepienie')
    ]
    AGGREGATE_STATES = [
        (SOLID, 'Stały'),
        (LIQUID, 'Płynny')
    ]
    name = models.CharField(max_length=50)
    quantity = models.FloatField(default=0)
    type = models.CharField(max_length=15, choices=MEDICATION_TYPES, default=DRUG)
    aggregate_state = models.CharField(max_length=15, choices=AGGREGATE_STATES, default=LIQUID)
    price = models.FloatField(default=1)
    date = models.DateTimeField(auto_now=True)
    farm = models.ForeignKey(Farm, on_delete=CASCADE)


class MedicationSupply(models.Model):
    medication = models.ForeignKey(Medication, on_delete=CASCADE)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    cycle_day = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)



class StoredFeed(models.Model):
    date = models.DateTimeField(auto_now=True)
    farm = models.ForeignKey(Farm, on_delete=CASCADE)
    price = models.FloatField(default=1)
    type = models.CharField(max_length=15)
    quantity = models.FloatField(default=0)


class Standard(models.Model):
    cycle_day = models.IntegerField(default=0)
    average_body_weight = models.FloatField(default=0)
    daily_weight_gain = models.FloatField(default=0)
    average_daily_weight_gain = models.FloatField(default=0)
    feed_consumption = models.FloatField(default=0)
    cumulative_feed_consumption = models.FloatField(default=0)
    water_consumption = models.FloatField(default=0)
    cumulative_wather_consumption = models.FloatField(default=0)
    feed_conversion = models.FloatField(default=0)

    def __str__(self):
        return str(self.cycle_day)

class MinRolPrices(models.Model):
    date = models.DateField(auto_now=True)
    price = models.FloatField(default=0)

    def __str__(self):
        return str(self.date)
