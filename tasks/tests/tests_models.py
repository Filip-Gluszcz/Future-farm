from django.test import Client, TestCase
from django.contrib.auth.models import User

from account.models import Farm
from tasks.models import Task

class TestModels(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User(username='Jan', email='jan@kowalski.pl')
        self.user.set_password('haslo123')
        self.user.save()
        self.client.login(username='Jan', password='haslo123')


    def test_task_model_str(self):
        farm1 = Farm.objects.create(
            name='farm1',
            max_herd_size=30000,
            surface=2000,
            user=self.user
        )
        task1 = Task.objects.create(
            text='test',
            user=self.user,
            farm=farm1
        )
        self.assertEqual(str(task1), 'test')