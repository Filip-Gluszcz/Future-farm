from django.contrib import admin
from production_cycle import models

# Register your models here.
admin.site.register(models.Day)
admin.site.register(models.Cycle)
admin.site.register(models.CycleCompleted)
admin.site.register(models.Standard)
admin.site.register(models.Slaughter)
admin.site.register(models.FeedDelivery)
admin.site.register(models.MinRolPrices)
admin.site.register(models.Medication)
admin.site.register(models.MedicationSupply)
admin.site.register(models.StoredFeed)
