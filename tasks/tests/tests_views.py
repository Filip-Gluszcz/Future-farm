from django.test import Client, TestCase
from django.contrib.auth.models import User

from django.urls import reverse
from account.models import Farm

from tasks.forms import TaskForm
from tasks.models import Task


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User(username='Jan', email='jan@kowalski.pl')
        self.user.set_password('haslo123')
        self.user.save()
        self.client.login(username='Jan', password='haslo123')

    def test_task_create_view_POST(self):
        farm1 = Farm.objects.create(
            name='farm1',
            max_herd_size=30000,
            surface=2000,
            user=self.user
        )
        response = self.client.post(reverse('createTask'), {
            'text': 'test', 
            'farm': farm1.id, 
            'status': 'NEW', 
            'important': False
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Task.objects.last().text, 'test')


    def test_farm_form_is_valid_true(self):
        farm1 = Farm.objects.create(
            name='farm1',
            max_herd_size=30000,
            surface=2000,
            user=self.user
        )
        form_data = {
            'text': 'test', 
            'farm': farm1.id, 
            'status': 'NEW', 
            'important': False
        }

        form = TaskForm(form_data)
        self.assertEquals(form.is_valid(), True)

    
    def test_tasks_list_view_GET(self):
        farm1 = Farm.objects.create(
            name='farm1',
            max_herd_size=30000,
            surface=2000,
            user=self.user
        )
        task1 = Task.objects.create(
            text='test',
            farm=farm1,
            user=self.user
        )

        response = self.client.get(reverse('tasks'))
        
        self.assertEquals(response.status_code, 200)
        
        context = response.context
        self.assertIn('farms', context)