from datetime import datetime
import email
from pprint import pprint
from urllib import response
from django.test import TestCase, Client,RequestFactory
from model_bakery import baker
from django.urls import reverse
from production_cycle.forms import DayForm, FeedDeliveryForm, SlaughterForm
from production_cycle.models import Cycle, FeedDelivery, MinRolPrices, Slaughter, Day, Standard
from production_cycle.views import CycleCreateView
from account.models import Farm
from tasks.models import Task
from django.contrib.auth.models import User

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User(username='Jan', email='jan@kowalski.pl')
        self.user.set_password('haslo123')
        self.user.save()
        self.client.login(username='Jan', password='haslo123')

    #CYCLE TESTS
        
    def test_cycle_detail_view_GET(self):
        farm1 = Farm.objects.create(
            name='farm1',
            max_herd_size=30000,
            surface=2000,
            user=self.user
        )
        cycle1 = Cycle.objects.create(           
           herd_size=25000,
           current_herd_size=20000,
           farm=farm1,
        
        )
        day1= Day.objects.create(
            cycle_day=0,
            deads=10,
            selection=10,
            daily_mortality_rate=0.0,
            feed_consumption=60,
            daily_wather_consumption=40,
            average_body_weight=43,
            temperature=30,
            humidity=60,
            medications='brak',
            cycle=cycle1,
            eww=0,
            fcr=0,
            total_feed=1000,
            total_water=1000,
            water_meter_value=1000,
            increasing_feed_consumption=1100,
        )


        standards1 = Standard.objects.create(
            cycle_day=0
        )

        standards2 = Standard.objects.create(
            cycle_day=1
        )
        standards3 = Standard.objects.create(
            cycle_day=2
        )

        minrol1 = MinRolPrices.objects.create(
            price=4238
        )
        minrol2 = MinRolPrices.objects.create(
            price=4338
        )

        task1 = Task.objects.create(
            text='tasktestowy',
            important=True,
            farm=farm1,
            user=self.user
        )

        response = self.client.get(reverse('cycleDetail', args=[cycle1.id]))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'production_cycle/cycle/cycles.html')
        
        context = response.context
        self.assertIn('standards', context)
        self.assertIn('lastDay', context)
        self.assertIn('daysRange', context)
        self.assertIn('nextDayNumber', context)
        self.assertIn('nextDayStats', context)
        self.assertIn('remainingDays', context)
        self.assertIn('statsRangeEnd', context)
        self.assertIn('sizePercent', context)
        self.assertIn('tasks', context)
        self.assertIn('tasksCount', context)
        self.assertIn('minrol', context)
        self.assertIn('minrolsDifference', context)
        self.assertIn('minrolRounded', context)
        self.assertIn('userFullName', context)
        

    def test_cycle_create_view_POST(self):
        farm1 = Farm.objects.create(
            name='farm1',
            max_herd_size=30000,
            surface=2000,
            user=self.user
        )
        response = self.client.post(reverse('createCycle', args=[farm1.id]), {
            'hybryd': 'hybryd',
            'herd_size': 30000,
            'chick_avarage_weight': 40,
            'age_of_the_reproductive_stock': '23',
            'hatchery': 'hatchery',
            'water_meter_value': 0,
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(farm1.cycle_set.first().hybryd, 'hybryd')
        
    
    def test_cycle_delete_view_DELETE(self):
        farm1 = Farm.objects.create(
            name='farm1',
            max_herd_size=30000,
            surface=2000,
            user=self.user
        )
        cycle1 = Cycle.objects.create(           
           herd_size=25000,
           current_herd_size=20000,
           farm=farm1,
        
        )
        response = self.client.delete(reverse('deleteCycle', args=[cycle1.id]))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(farm1.cycle_set.count(), 0)


    #SLAUGHTER TESTS
    def test_slaughter_create_view_POST(self):
        farm1 = Farm.objects.create(
            name='farm1',
            max_herd_size=30000,
            surface=2000,
            user=self.user
        )
        cycle1 = Cycle.objects.create(           
           herd_size=25000,
           current_herd_size=20000,
           farm=farm1,
        
        )

        response = self.client.post(reverse('createSlaughter', args=[cycle1.id]), {
            'date': datetime.now(),
            'cycle': cycle1,
            'day_id': 1,
            'quantity': 5000,
            'weight': 13500,
            'average_weight': 2.7,
            'slaughterhouse': 'slaughterhouse'
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(cycle1.slaughter_set.first().quantity, 5000)

    
    def test_slaughter_form_valid_is_true(self):
        
        form_data = {
            'day_id': 1,
            'quantity': 5000,
            'weight': 13500,
            'average_weight': 2.7,
            'slaughterhouse': 'slaughterhouse'
        }

        farm1 = Farm.objects.create(
            name='farm1',
            max_herd_size=30000,
            surface=2000,
            user=self.user
        )
        cycle1 = Cycle.objects.create(           
           herd_size=25000,
           current_herd_size=20000,
           farm=farm1,
        
        )

        form = SlaughterForm(form_data)
        form.instance.cycle = cycle1

        self.assertEquals(form.is_valid(), True)



    #FEED DELIVERY TESTS
    def test_feeddelivery_create_view_POST(self):
        farm1 = Farm.objects.create(
            name='farm1',
            max_herd_size=30000,
            surface=2000,
            user=self.user
        )
        cycle1 = Cycle.objects.create(           
           herd_size=25000,
           current_herd_size=20000,
           farm=farm1,
        
        )

        response = self.client.post(reverse('createFeedDelivery', args=[cycle1.id]), {
            'date': datetime.now(),
            'cycle': cycle1,
            'choices': 'ST',
            'quantity': 5000,
            'price': 1300,
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(cycle1.feeddelivery_set.first().quantity, 5000)

    
    def test_feeddelivery_form_valid_is_true(self):
        
        form_data = {         
            'choices': 'ST',
            'quantity': 5000,
            'price': 1300,
        }

        farm1 = Farm.objects.create(
            name='farm1',
            max_herd_size=30000,
            surface=2000,
            user=self.user
        )
        cycle1 = Cycle.objects.create(           
           herd_size=25000,
           current_herd_size=20000,
           farm=farm1,
        
        )

        form = FeedDeliveryForm(form_data)
        form.instance.cycle = cycle1

        self.assertEquals(form.is_valid(), True)



    #DAY TESTS
    def test_day_create_view_POST(self):
        farm1 = Farm.objects.create(
            name='farm1',
            max_herd_size=30000,
            surface=2000,
            user=self.user
        )
        cycle1 = Cycle.objects.create(           
           herd_size=25000,
           current_herd_size=20000,
           farm=farm1,
        
        )
        standard1 = Standard.objects.create(
            cycle_day = 0,
            water_consumption = 1
        )
        standard2 = Standard.objects.create(
            cycle_day = 1,
            water_consumption = 1
        )
        standard3 = Standard.objects.create(
            cycle_day = 2,
            water_consumption = 1
        )
        day1 = Day.objects.create(
            cycle = cycle1,
            cycle_day=0
        )

        response = self.client.post(reverse('createDay', args=[cycle1.id]), {
            'cycle_day': 1,
            'deads': 25,            
            'selection': 20,
            'water_meter_value': 1500,
            'average_body_weight': 1300,
            'temperature': 32,
            'humidity': 60,
            'medications': 'brak', 
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(cycle1.day_set.last().deads, 25)


    def test_day_form_valid_is_true(self):
        form_data = {
            'cycle_day': 1,
            'deads': 25,            
            'selection': 20,
            'water_meter_value': 1500,
            'average_body_weight': 1300,
            'temperature': 32,
            'humidity': 60,
            'medications': 'brak',
        }

        farm1 = Farm.objects.create(
            name='farm1',
            max_herd_size=30000,
            surface=2000,
            user=self.user
        )
        cycle1 = Cycle.objects.create(           
           herd_size=25000,
           current_herd_size=20000,
           farm=farm1,
        
        )
        day1 = Day.objects.create(
            cycle = cycle1
        )

        form = DayForm(form_data)
        form.instance.cycle = cycle1

        self.assertEquals(form.is_valid(), True)

#  coverage run --omit='*/env/*' manage.py test