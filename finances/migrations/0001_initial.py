# Generated by Django 3.1.4 on 2022-03-01 23:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('production_cycle', '0001_initial'),
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('worth', models.FloatField(default=0)),
                ('category', models.CharField(choices=[('Pasza', 'Pasza'), ('Farmaceutyk', 'Farmaceutyk'), ('Stado', 'Stado'), ('Ubój', 'Ubój'), ('Inne', 'Inne')], default='Inne', max_length=15)),
                ('type', models.CharField(choices=[('Przychód', 'Przychód'), ('Wydatek', 'Wydatek')], default='Wydatek', max_length=15)),
                ('recipient_sender', models.CharField(max_length=35)),
                ('internal', models.BooleanField(default=False)),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production_cycle.cycle')),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.farm')),
            ],
        ),
        migrations.CreateModel(
            name='ToAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('worth', models.FloatField(default=0)),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production_cycle.cycle')),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.farm')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FarmFinance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_revenues', models.FloatField(default=0)),
                ('total_expenses', models.FloatField(default=0)),
                ('total_balance', models.FloatField(default=0)),
                ('total_contributions', models.FloatField(default=0)),
                ('total_withdrawal', models.FloatField(default=0)),
                ('farm', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.farm')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyFinance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_revenues', models.FloatField(default=0)),
                ('total_expenses', models.FloatField(default=0)),
                ('total_balance', models.FloatField(default=0)),
                ('total_contributions', models.FloatField(default=0)),
                ('total_withdrawal', models.FloatField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
