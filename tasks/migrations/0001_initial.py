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
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('text', models.CharField(max_length=100)),
                ('important', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('NEW', 'New'), ('DURING', 'During'), ('DONE', 'Done')], default='NEW', max_length=6)),
                ('farm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.farm')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
