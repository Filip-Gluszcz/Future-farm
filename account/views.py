
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from finances.models import CompanyFinance

from production_cycle.models import Cycle, Standard, StoredFeed
from .forms import ActivateSiloForm, AdditionalFeedForm, EmptyFeedForm, FarmForm, ProfileForm, RegisterForm, SiloForm, UserUpdateForm
from .models import Farm, Profile, Silo
from tasks.models import Task


class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'account/profile/create.html'
    success_url = reverse_lazy('farmList')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AccountDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile/detail.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    context_object_name = 'user'
    form_class = UserUpdateForm
    success_url = reverse_lazy('account')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    context_object_name = 'profile'
    form_class = ProfileForm
    success_url = reverse_lazy('account')


class UserRegistration(FormView):
    model = User
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('createProfile')

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return redirect('login')


class FarmCreateView(LoginRequiredMixin, CreateView):
    model = Farm
    form_class = FarmForm
    template_name = 'account/farm/create.html'
    success_url = reverse_lazy('farmList')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FarmDeleteView(LoginRequiredMixin, DeleteView):
    model = Farm
    template_name = 'account/farm/delete.html'
    success_url = reverse_lazy('farmList')


class FarmUpdateView(LoginRequiredMixin, UpdateView):
    model = Farm
    context_object_name = 'farm'
    form_class = FarmForm
    template_name = 'account/farm/update.html'
    success_url = reverse_lazy('farmList')


class FarmListView(LoginRequiredMixin, ListView):
    model = Farm
    template_name = 'account/farm/list.html'
    context_object_name = 'farms'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['farms'] = context['farms'].filter(user=self.request.user)
        
        statsRange = []        
        context['activeCycles'] = 0
        context['closedCycles'] = 0
        for farm in context['farms']:
            context['activeCycles'] += farm.cycle_set.filter(status='ACTIVE').count()
            context['closedCycles'] += farm.cycle_set.filter(status='CLOSED').count()
            if farm.cycle_set.all().count() > 0:
                if farm.cycle_set.last().day_set.all().count() > 0:
                    statsRange.append(farm.cycle_set.last().day_set.last().cycle_day)
        if statsRange:
            context['statsEnd'] = max(statsRange)
        else:
            context['statsEnd'] = 5
        context['standards'] = Standard.objects.all()
        context['userFullName'] = self.request.user.get_full_name()
        context['tasksCount'] = Task.objects.filter(user=self.request.user).count()
        context['newTasks'] = Task.objects.filter(status='NEW', user=self.request.user)
        context['duringTasks'] = Task.objects.filter(status='DURING',  user=self.request.user)
        context['doneTasks'] = Task.objects.filter(status='DONE',  user=self.request.user)
        context['companyFinance'] = CompanyFinance.objects.get(user=self.request.user)

        return context


class SiloCreateView(LoginRequiredMixin, CreateView):

    model = Silo
    form_class = SiloForm
    template_name = 'account/silo/create.html'
    success_url = reverse_lazy('farmList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['farms'] = Farm.objects.filter(user=self.request.user)
        return context


class SiloUpdateView(LoginRequiredMixin, UpdateView):
    model = Silo
    context_object_name = 'silo'
    form_class = SiloForm
    template_name = 'account/silo/create.html'
    success_url = reverse_lazy('farmList')


class SiloDeleteView(LoginRequiredMixin, DeleteView):
    model = Silo
    # template_name = 'account/silo/create.html'
    success_url = reverse_lazy('farmList')


class SiloListView(LoginRequiredMixin, ListView):
    model = Silo
    context_object_name = 'silos'
    template_name = 'account/silo/silos.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        farm = Farm.objects.get(id=self.kwargs.get('farmId'))
        context['silos'] = context['silos'].filter(farm=farm)
        context['storedFeeds'] = StoredFeed.objects.filter(farm=farm)
        cycle = Cycle.objects.filter(farm=farm).last()
        context['cycle'] = cycle
        standards = Standard.objects.filter(cycle_day__gte=cycle.day_set.last().cycle_day)
        try:
            context['activeSilo'] = Silo.objects.get(active=True, farm=farm)
            context['lastFeedDelivery'] = context['activeSilo'].feeddelivery_set.last()
            for standard in standards:
                if cycle.day_set.all().count() > 1:
                    last_day = cycle.day_set.last()
                    lastDayStandard = Standard.objects.get(cycle_day=last_day.cycle_day)
                    if ((cycle.current_herd_size * (standard.cumulative_feed_consumption / 1000)) * (last_day.feed_consumption / lastDayStandard.feed_consumption)) > context['activeSilo'].state + last_day.total_increasing_feed_consumption:
                        context['daysLeft'] = standard.cycle_day - last_day.cycle_day
                        break
                else:
                    if (cycle.current_herd_size * (standard.cumulative_feed_consumption / 1000)) > context['activeSilo'].state + last_day.total_increasing_feed_consumption:
                        context['daysLeft'] = standard.cycle_day
                        break

        except Silo.DoesNotExist:
            context['activeSilo'] = None            
            context['lastFeedDelivery'] = None

        return context


class SiloActivateView(LoginRequiredMixin, UpdateView):
    model = Silo
    context_object_name = 'silo'
    form_class = ActivateSiloForm
    template_name = 'account/silo/create.html'
    success_url = '/silos/{farm_id}'

    def form_valid(self, form):
        silos = Silo.objects.filter(farm=Farm.objects.get(id=self.kwargs.get('farmId')))
        for silo in silos:
            if silo.id != int(self.kwargs.get('pk')):
                silo.active = False
                silo.save()
        return super().form_valid(form)


class SiloDeactivateView(LoginRequiredMixin, UpdateView):
    model = Silo
    context_object_name = 'silo'
    form_class = ActivateSiloForm
    template_name = 'account/silo/create.html'
    success_url = '/silos/{farm_id}'


class AdditionalFeedView(LoginRequiredMixin, FormView):
    form_class = AdditionalFeedForm

    def get_success_url(self):
        return reverse('silos', kwargs={'farmId': self.kwargs['farmId']})

    def form_valid(self, form):
        activeSilo = Silo.objects.get(id=form.cleaned_data['activeSiloId'])
        standard = Standard.objects.get(cycle_day=form.cleaned_data['cycleDay'] + 1)
        herdSize = form.cleaned_data['herdSize']
        activeSilo.state += (standard.feed_consumption * herdSize) / 1000
        activeSilo.save()
        return super().form_valid(form)


class EmptyFeedView(LoginRequiredMixin, FormView):
    form_class = EmptyFeedForm

    def get_success_url(self):
        return reverse('silos', kwargs={'farmId': self.kwargs['farmId']})

    def form_valid(self, form):
        activeSilo = Silo.objects.get(id=form.cleaned_data['activeSiloId'])
        activeSilo.state = 0
        activeSilo.save()
        return super().form_valid(form)

