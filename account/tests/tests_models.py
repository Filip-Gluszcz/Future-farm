from django.test import Client, TestCase
from account.models import Farm
from model_bakery import baker
from django.contrib.auth.models import User

class TestModels(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User(username='Jan', email='jan@kowalski.pl')
        self.user.set_password('haslo123')
        self.user.save()
        self.client.login(username='Jan', password='haslo123')

    def test_farm_model_str(self):
        farm = Farm.objects.create(
            name='farm',
            user=self.user
        )

        self.assertEqual(str(farm), 'farm')