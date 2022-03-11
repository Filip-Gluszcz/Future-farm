from django.test import TestCase
from production_cycle.models import Day, Standard
from model_bakery import baker

class TestModels(TestCase):

    #DAY TEST
    def test_day_model_str(self):
        cycle = baker.make('production_cycle.Cycle')
        cycle.id = 1
        cycle.herd_size = 20000
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
        day0 = Day.objects.create(
            cycle_id = cycle.id,
            cycle_day = 0,
            average_body_weight = 42
        )
        day1 = Day.objects.create(
            cycle_id = cycle.id,
            cycle_day = 1,
            average_body_weight = 52
        )
        self.assertEqual(str(day1), '1')

    #CYCLE TEST
    def test_cycle_model_str(self):
        cycle = baker.make('production_cycle.Cycle')
        name = str(cycle.date_of_insertion)
        self.assertEqual(str(cycle), name)

    #STANDARD TEST
    def test_standard_model_str(self):
        standard = baker.make('production_cycle.Standard')
        standard.cycle_day = 8
        self.assertEqual(str(standard), '8')

    #MINROLPRICES TEST
    def test_minrolprices_model_str(self):
        minrol = baker.make('production_cycle.MinRolPrices')
        self.assertEqual(str(minrol), str(minrol.date))