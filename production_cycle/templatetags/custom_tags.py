from django import template

from account.models import Silo
from production_cycle.models import Cycle
from finances.models import Transaction

register = template.Library()


@register.simple_tag
def multiply(a, b, *args, **kwargs):
    return a * b

@register.simple_tag
def sum(a, b, *args, **kwargs):
    return a + b

@register.simple_tag
def divide(a, b, *args, **kwargs):
    return round(a / b, 2)

@register.simple_tag
def rounded(a, *args, **kwargs):
    return round(a, 2)

@register.simple_tag
def specyficRounded(a, b, *args, **kwargs):
    return round(a, b)

@register.simple_tag
def active_silo_filter(queryset, *args, **kwargs):
    try:
       filtered = queryset.filter(active=True)
    except Silo.DoesNotExist:
        filtered = None
    return filtered

@register.simple_tag
def last_cycle_total_revenues(a, *args, **kwargs):
    total_revenues = 0
    # cycle = Cycle.objects.get(id=a)
    try:
        cycle_revenues = a.transaction_set.filter(type='Przychód')
        for transaction in cycle_revenues:
            total_revenues += transaction.worth
    except Transaction.DoesNotExist:
        total_revenues = 0
    return total_revenues

@register.simple_tag
def last_cycle_total_expenses(a, *args, **kwargs):
    total_expenses = 0
    # cycle = Cycle.objects.get(id=a)
    try:
        cycle_expenses = a.transaction_set.filter(type='Wydatek')
        for transaction in cycle_expenses:
            total_expenses += transaction.worth
    except Transaction.DoesNotExist:
        total_expenses = 0
    return total_expenses


@register.simple_tag
def get_id(a, *args, **kwargs):
    print(a)
    id = a
    return str(id)

    #onclick="location.href='{% url 'cycleDetail' 10 %}'"
    # onClick: function(e){
    #         var element = this.getElementAtEvent(e);
    #         location.href=`/cycle-detail/${element.id}`
    #     },