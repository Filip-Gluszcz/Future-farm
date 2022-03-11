from django.contrib import admin

from finances.models import CompanyFinance, ToAccount, FarmFinance, Transaction

# Register your models here.
admin.site.register(CompanyFinance)
admin.site.register(FarmFinance)
admin.site.register(Transaction)
admin.site.register(ToAccount)