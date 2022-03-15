from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Farm, Profile, Silo


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class FarmForm(ModelForm):
    class Meta:
        model = Farm
        fields = ['name', 'max_herd_size', 'surface']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['nip', 'regon', 'city', 'street', 'number', 'postal_code']
        # widgets = {
        #     'myfield': forms.TextInput(attrs={'class': 'myfieldclass'}),
        # }

class SiloForm(ModelForm):
    class Meta:
        model = Silo
        fields = ['number', 'capacity', 'feet_type', 'state', 'farm']

class ActivateSiloForm(ModelForm):
    class Meta:
        model = Silo
        fields = ['active']

class AdditionalFeedForm(forms.Form):
    activeSiloId = forms.IntegerField()
    cycleDay = forms.IntegerField()
    herdSize = forms.IntegerField()
    
class EmptyFeedForm(forms.Form):
    activeSiloId = forms.IntegerField()