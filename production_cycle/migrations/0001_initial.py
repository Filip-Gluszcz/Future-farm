# Generated by Django 3.1.4 on 2022-03-01 23:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_insertion', models.DateTimeField(auto_now=True)),
                ('hybryd', models.CharField(default='hybryd', max_length=30)),
                ('herd_size', models.IntegerField(default=0)),
                ('chick_avarage_weight', models.FloatField(default=0)),
                ('age_of_the_reproductive_stock', models.CharField(default='age', max_length=30)),
                ('hatchery', models.CharField(default='hatchery', max_length=30)),
                ('current_herd_size', models.IntegerField(default=0)),
                ('water_meter_value', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('CLOSED', 'Closed')], default='ACTIVE', max_length=7)),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.farm')),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('cycle_day', models.IntegerField(default=0)),
                ('deads', models.IntegerField(default=0)),
                ('selection', models.IntegerField(default=0)),
                ('daily_mortality_rate', models.FloatField(default=0)),
                ('feed_consumption', models.FloatField(default=0)),
                ('daily_wather_consumption', models.FloatField(default=0)),
                ('average_body_weight', models.FloatField(default=0)),
                ('temperature', models.FloatField(default=0)),
                ('humidity', models.FloatField(default=0)),
                ('eww', models.FloatField(default=0)),
                ('fcr', models.FloatField(default=0)),
                ('total_feed', models.FloatField(default=0)),
                ('total_water', models.FloatField(default=0)),
                ('water_meter_value', models.FloatField(default=0)),
                ('increasing_feed_consumption', models.FloatField(default=0)),
                ('total_increasing_feed_consumption', models.FloatField(default=0)),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production_cycle.cycle')),
            ],
            options={
                'ordering': ('cycle_day',),
            },
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('quantity', models.FloatField(default=0)),
                ('type', models.CharField(choices=[('Lek', 'Lek'), ('Suplement', 'Suplement'), ('Szczepienie', 'Szczepienie')], default='Lek', max_length=15)),
                ('aggregate_state', models.CharField(choices=[('Stały', 'Stały'), ('Płynny', 'Płynny')], default='Płynny', max_length=15)),
                ('price', models.FloatField(default=1)),
                ('date', models.DateTimeField(auto_now=True)),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.farm')),
            ],
        ),
        migrations.CreateModel(
            name='MinRolPrices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('price', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Standard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cycle_day', models.IntegerField(default=0)),
                ('average_body_weight', models.FloatField(default=0)),
                ('daily_weight_gain', models.FloatField(default=0)),
                ('average_daily_weight_gain', models.FloatField(default=0)),
                ('feed_consumption', models.FloatField(default=0)),
                ('cumulative_feed_consumption', models.FloatField(default=0)),
                ('water_consumption', models.FloatField(default=0)),
                ('cumulative_wather_consumption', models.FloatField(default=0)),
                ('feed_conversion', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='StoredFeed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('price', models.FloatField(default=1)),
                ('type', models.CharField(max_length=15)),
                ('quantity', models.FloatField(default=0)),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.farm')),
            ],
        ),
        migrations.CreateModel(
            name='Slaughter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('day_id', models.CharField(max_length=50)),
                ('quantity', models.IntegerField(default=0)),
                ('weight', models.FloatField(default=0)),
                ('average_weight', models.FloatField(default=0)),
                ('slaughterhouse', models.CharField(max_length=50)),
                ('price', models.FloatField(default=1)),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production_cycle.cycle')),
            ],
        ),
        migrations.CreateModel(
            name='MedicationSupply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0)),
                ('cycle_day', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production_cycle.cycle')),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production_cycle.day')),
                ('medication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production_cycle.medication')),
            ],
        ),
        migrations.CreateModel(
            name='FeedDelivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('choices', models.CharField(choices=[('Starter', 'Starter'), ('Grower', 'Grower'), ('Finisher', 'Finisher')], default='Starter', max_length=15)),
                ('quantity', models.FloatField(default=0)),
                ('price', models.FloatField(default=1)),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production_cycle.cycle')),
                ('silo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.silo')),
            ],
        ),
        migrations.CreateModel(
            name='CycleCompleted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_weight', models.FloatField(default=1)),
                ('number_of_units_sold', models.IntegerField(default=1)),
                ('average_weight', models.FloatField(default=1)),
                ('total_feed', models.FloatField(default=1)),
                ('survival_rate', models.FloatField(default=1)),
                ('total_days', models.IntegerField(default=1)),
                ('fcr', models.FloatField(default=1)),
                ('eww', models.FloatField(default=1)),
                ('total_revenues', models.FloatField(default=0)),
                ('total_expenses', models.FloatField(default=0)),
                ('total_balance', models.FloatField(default=0)),
                ('cycle', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='production_cycle.cycle')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
