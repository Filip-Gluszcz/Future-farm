from re import template
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from account.models import Farm
from production_cycle.models import Cycle, CycleCompleted, MinRolPrices, Standard
from .models import CompanyFinance, FarmFinance, ToAccount, Transaction
from .forms import TransactionForm


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('finances')


class ToAccountTransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = '/Users/FilipGluszcz/Desktop/PZRepo/Praca-dyplomowa/production_cycle/templates/production_cycle/cycle/create.html'
    success_url = reverse_lazy('finances')

    def form_valid(self, form):
        toAccount = ToAccount.objects.get(id=self.kwargs.get('toAccountId'))
        toAccount.delete()
        return super().form_valid(form)

class ToAccountTransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = ToAccount
    success_url = reverse_lazy('finances')

class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('finances')


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy('finances')


class FarmFinanceListView(LoginRequiredMixin, ListView):
    model = FarmFinance
    context_object_name = 'farmFinances'
    template_name = 'finances/list.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['farmFinances'] = context['farmFinances'].filter(user=self.request.user)
        context['companyFinance'] = CompanyFinance.objects.get(user=self.request.user)
        context['closedCycles'] = CycleCompleted.objects.filter(user=self.request.user)
        context['toAccountList'] = ToAccount.objects.filter(user=self.request.user)
        context['minRol'] = MinRolPrices.objects.last()
        context['standardAverageWeight'] = Standard.objects.get(cycle_day=42).average_body_weight
        
        return context