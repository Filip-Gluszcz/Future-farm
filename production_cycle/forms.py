from django import forms
from django.db.models import fields
from django.forms import ModelForm
from .models import CycleCompleted, Day, Cycle, FeedDelivery, Medication, MedicationSupply, Slaughter, StoredFeed


class DayForm(ModelForm):
    class Meta:
        model = Day
        fields = ['cycle_day', 'deads', 'selection', 'water_meter_value',
                  'average_body_weight', 'temperature', 'humidity']

        # def __init__(self, fields, cycle):
        #     self.fields = fields
        #     self.model.cycle = cycle


class CycleForm(ModelForm):
    class Meta:
        model = Cycle
        fields = ['hybryd', 'herd_size', 'chick_avarage_weight',
                  'age_of_the_reproductive_stock', 'hatchery', 'water_meter_value']


class SlaughterForm(ModelForm):
    class Meta:
        model = Slaughter
        fields = ['day_id', 'quantity', 'weight', 'slaughterhouse']


class FeedDeliveryForm(ModelForm):
    class Meta:
        model = FeedDelivery
        fields = ['choices', 'quantity', 'price', 'silo']


class StoredFeedForm(ModelForm):
    class Meta:
        model = StoredFeed
        fields = ['price', 'type', 'quantity']


class MedicationForm(ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'quantity', 'type', 'aggregate_state', 'price']


class MedicationSupplyForm(ModelForm):
    class Meta:
        model = MedicationSupply
        fields = ['medication', 'quantity', 'cycle_day', 'cycle']


class CycleCompletedForm(ModelForm):
    class Meta:
        model = CycleCompleted
        fields = ['total_weight', 'number_of_units_sold', 'average_weight', 'total_feed', 'survival_rate', 'total_days']


class RestoreFeedForm(forms.Form):
    storedFeedId = forms.IntegerField()
    siloId = forms.IntegerField()
    type = forms.CharField(max_length=15)
    quantity = forms.FloatField()

# E67E22
