from django.forms import ModelForm
from finances.models import Transaction, ToAccount

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'worth', 'category', 'type', 'recipient_sender', 'internal', 'farm', 'cycle']


class ToAccountForm(ModelForm):
    class Meta:
        model = ToAccount
        fields = ['title', 'worth']