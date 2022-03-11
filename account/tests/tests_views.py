from django.test import Client, TestCase
from django.urls import reverse
from account.forms import FarmForm, ProfileForm, RegisterForm
from account.models import Farm, Profile
from model_bakery import baker
from django.contrib.auth.models import User

class TestModels(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User(username='Jan', email='jan@kowalski.pl')
        self.user.set_password('haslo123')
        self.user.save()
        self.client.login(username='Jan', password='haslo123')


    def test_profile_create_view_POST(self):
        response = self.client.post(reverse('createProfile'), {
            'nip': 13212132, 
            'regon':2331211, 
            'city': 'city1', 
            'street': 'street1', 
            'number': 23, 
            'postal_code': 23456 
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.user.profile.nip, 13212132)
    
    def test_profile_form_is_valid_true(self):
        form_data = {
            'nip': 13212132, 
            'regon':2331211, 
            'city': 'city1', 
            'street': 'street1', 
            'number': 23, 
            'postal_code': 23456
        }

        form = ProfileForm(form_data)
        form.instance.user = self.user

        self.assertEquals(form.is_valid(), True)


    def test_user_create_view_POST(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'name', 
            'last_name': 'surname', 
            'username': 'username1', 
            'email': 'email@email.com', 
            'password1': 'testowe123', 
            'password2': 'testowe123'
        })

        self.assertEquals(response.status_code, 302)
        users = User.objects.all()
        self.assertEquals(users.count(), 2)


    def test_user_register_form_is_valid_true(self):
        form_data = {
            'first_name': 'name', 
            'last_name': 'surname', 
            'username': 'username1', 
            'email': 'email@email.com', 
            'password1': 'testowe123', 
            'password2': 'testowe123'
        }

        form = RegisterForm(form_data)
        self.assertEquals(form.is_valid(), True)


    def test_farm_create_view_POST(self):
        response = self.client.post(reverse('createFarm'), {
            'name': 'farm1', 
            'max_herd_size': 3000, 
            'surface': 2000 
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.user.farm_set.last().name, 'farm1')


    def test_farm_form_is_valid_true(self):
        form_data = {
            'name': 'farm1', 
            'max_herd_size': 3000, 
            'surface': 2000 
        }

        form = FarmForm(form_data)
        self.assertEquals(form.is_valid(), True)

    def test_farm_list_view_GET(self):
        farm1 = Farm.objects.create(
            name='farm1',
            max_herd_size=30000,
            surface=2000,
            user=self.user
        )
        farm2 = Farm.objects.create(
            name='farm2',
            max_herd_size=40000,
            surface=2500,
            user=self.user
        )

        response = self.client.get(reverse('farmList'))
        
        self.assertEquals(response.status_code, 200)
        
        context = response.context
        self.assertIn('farms', context)