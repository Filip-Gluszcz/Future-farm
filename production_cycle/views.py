from django.shortcuts import redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.signals import post_delete, post_save, pre_save, pre_delete
from django.dispatch import Signal, receiver
from django.db.models import Sum
from django.urls import reverse, reverse_lazy
import csv

from tasks.models import Task
from .models import *
from .forms import *


#CYCLE VIEWS
class CycleListView(LoginRequiredMixin, ListView):
    model = Cycle
    template_name = 'production_cycle/cycle/cycles.html'
    context_object_name = 'cycles'


class CycleCreateView(LoginRequiredMixin, CreateView):
    model = Cycle
    form_class = CycleForm
    template_name = 'production_cycle/cycle/create.html'
    success_url = reverse_lazy('farmList')

    def form_valid(self, form):
        user = self.request.user
        form.instance.farm = user.farm_set.get(
            id=self.kwargs.get('id'))
        form.instance.current_herd_size = form.instance.herd_size
        return super().form_valid(form)


class CycleDetailView(LoginRequiredMixin, DetailView):
    model = Cycle
    context_object_name = 'cycle'
    template_name = 'production_cycle/cycle/cycles.html'

    def get(self, request, *args, **kwargs):
        cycle = Cycle.objects.get(id=self.kwargs['pk'])
        farm = cycle.farm
        if farm.user != request.user:
            return redirect(reverse_lazy('farmList'))
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['standards'] = Standard.objects.all()

        context['lastDay'] = context['cycle'].day_set.last()
        # context['lastDay'] = Day.objects.filter(cycle=context['cycle']).last()
        if context['lastDay'] != None:
            if context['lastDay'].cycle_day < 4:
                context['daysRange'] = range(4 - context['lastDay'].cycle_day)

            if context['lastDay'].cycle_day < 49:
                context['nextDayNumber'] = context['lastDay'].cycle_day + 1
                context['nextDayStats'] = Standard.objects.get(cycle_day=context['nextDayNumber'])
                context['projectedFeedConsumption'] = (context['nextDayStats'].feed_consumption * context['cycle'].current_herd_size) / 1000
            
            context['remainingDays'] = 49 - context['lastDay'].cycle_day
            context['totalFeed'] = context['lastDay'].total_increasing_feed_consumption
            if context['cycle'].feeddelivery_set.all().count() > 0:
                context['totalFeedDelivery'] = FeedDelivery.objects.filter(cycle=context['cycle']).aggregate(Sum('quantity'))['quantity__sum'] * 1000
            else:
                context['totalFeedDelivery'] = 0
        
        if context['cycle'].herd_size > 0:
            context['sizePercent'] = int((
                    context['cycle'].current_herd_size / context['cycle'].herd_size) * 100)
        context['tasks'] = Task.objects.filter(user=self.request.user, farm=context['cycle'].farm)
        newTasksCount = Task.objects.filter(user=self.request.user, farm=context['cycle'].farm, status='NEW').count()
        duringTasksCount = Task.objects.filter(user=self.request.user, farm=context['cycle'].farm, status='DURING').count()
        context['tasksCount'] = newTasksCount + duringTasksCount
        context['minrol'] = MinRolPrices.objects.last()
        if MinRolPrices.objects.all().count() >= 2:
            context['minrolsDifference'] = round((context['minrol'].price - MinRolPrices.objects.all().order_by('-id')[1].price)/10)
        context['minrolRounded'] = round((context['minrol'].price)/1000, 2)
        context['userFullName'] = self.request.user.get_full_name()

        try:
            context['acttiveSilo'] = Silo.objects.get(farm=context['cycle'].farm, active=True)
        except Silo.DoesNotExist:
            context['acttiveSilo'] = None

        context['medications'] = Medication.objects.filter(farm=context['cycle'].farm)
        context['supplies'] = MedicationSupply.objects.filter(cycle=context['cycle'])
        
        context['totalWeight'] = 0
        context['totalSoldUnits'] = 0
        if context['cycle'].slaughter_set.all().count() > 0:
            for slaughter in context['cycle'].slaughter_set.all():
                context['totalWeight'] += slaughter.weight
                context['totalSoldUnits'] += slaughter.quantity
            
            context['averageWeight'] = round(context['totalWeight'] / context['totalSoldUnits'], 3)

        try:
            context['cycleCompleted'] = CycleCompleted.objects.get(cycle=context['cycle'])
        except CycleCompleted.DoesNotExist:
            context['cycleCompleted'] = None

        total_deads = 0
        for day in context['cycle'].day_set.all():
            total_deads += day.deads + day.selection

        context['survivalRate'] = round(((context['cycle'].herd_size - total_deads) / context['cycle'].herd_size) * 100, 2)
        
        return context


class CycleDeleteView(LoginRequiredMixin, DeleteView):
    model = Cycle
    success_url = reverse_lazy('farmList')
    template_name = 'production_cycle/cycle/delete.html'
    # context_object_name = 'cycle'


class CycleUpdateView(LoginRequiredMixin, UpdateView):
    model = Cycle
    form_class = CycleForm
    template_name = 'production_cycle/cycle/update.html'
    success_url = reverse_lazy('farmList')



#FEED DELIVERY VIEWS
class FeedDeliveryCreateView(LoginRequiredMixin, CreateView):
    model = FeedDelivery
    form_class = FeedDeliveryForm
    template_name = 'production_cycle/feed_delivery/create.html'
    
    def get_success_url(self):
        return reverse('silos', kwargs={'farmId': self.kwargs['farmId']})

    def form_valid(self, form):
        form.instance.cycle = Cycle.objects.get(id=self.kwargs.get('cycleId'))
        form.instance.price *= 1.08
        return super().form_valid(form)


class FeedDeliveryDetailView(LoginRequiredMixin, DetailView):
    model = FeedDelivery
    template_name = 'production_cycle/feed_delivery/detail.html'


class FeedDeliveryListView(LoginRequiredMixin, ListView):
    model = FeedDelivery
    template_name = 'production_cycle/feed_delivery/List.html'


class FeedDeliveryUpdateView(LoginRequiredMixin, UpdateView):
    model = FeedDelivery
    form_class = FeedDeliveryForm
    template_name = 'production_cycle/feed_delivery/update.html'
    
    def get_success_url(self):
        return reverse('silos', kwargs={'farmId': self.kwargs['farmId']})


class FeedDeliveryDeleteView(LoginRequiredMixin, DeleteView):
    model = FeedDelivery
    template_name = 'production_cycle/feed_delivery/delete.html'
    
    def get_success_url(self):
        return reverse('silos', kwargs={'farmId': self.kwargs['farmId']})


#STORED FEED VIEWS
class StoredFeedCreateView(LoginRequiredMixin, CreateView):
    model = StoredFeed
    form_class = StoredFeedForm
    template_name = 'production_cycle/stored_feed/create.html'

    def get_success_url(self):
        return reverse('silos', kwargs={'farmId': self.kwargs['farmId']})

    def form_valid(self, form):
        form.instance.farm = Farm.objects.get(id=self.kwargs.get('farmId'))
        silo = Silo.objects.get(id=self.kwargs.get('siloId'))
        silo.state = 0
        silo.save()
        return super().form_valid(form)


class StoredFeedDeleteView(LoginRequiredMixin, DeleteView):
    model = StoredFeed

    def get_success_url(self):
        return reverse('silos', kwargs={'farmId': self.kwargs['farmId']})


class StoredFeedUpdateView(LoginRequiredMixin, UpdateView):
    model = StoredFeed
    form_class = StoredFeedForm
    template_name = 'production_cycle/stored_feed/create.html'

    def get_success_url(self):
        return reverse('silos', kwargs={'farmId': self.kwargs['farmId']})


class RestoreFeedView(LoginRequiredMixin, FormView):
    form_class = RestoreFeedForm

    def get_success_url(self):
        return reverse('silos', kwargs={'farmId': self.kwargs['farmId']})

    def form_valid(self, form):
        siloId = form.cleaned_data['siloId']
        storedFeedId = form.cleaned_data['storedFeedId']
        storedFeed = StoredFeed.objects.get(id=storedFeedId)
        silo = Silo.objects.get(id=siloId)
        silo.state += form.cleaned_data['quantity']
        silo.feet_type = form.cleaned_data['type']
        silo.save()
        storedFeed.delete()
        return super().form_valid(form)


#MEDICATION VIEWS
class MedicationCreateView(LoginRequiredMixin, CreateView):
    model = Medication
    form_class = MedicationForm
    success_url = '/medications/{farm_id}'
    template_name = 'production_cycle/medication/create.html'

    def form_valid(self, form):
        form.instance.farm = Farm.objects.get(id=self.kwargs.get('farmId'))
        return super().form_valid(form)

    
class MedicationUpdateView(LoginRequiredMixin, UpdateView):
    model = Medication
    form_class = MedicationForm
    success_url = '/medications/{farm_id}'    
    template_name = 'production_cycle/medication/create.html'


class MedicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Medication
    success_url = '/medications/{farm_id}'


class MedicationListView(LoginRequiredMixin, ListView):
    model = Medication
    template_name = 'production_cycle/medication/medications.html'
    context_object_name = 'medications'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        farm = Farm.objects.get(id=self.kwargs.get('farmId'))
        context['medications'] = Medication.objects.filter(farm=farm)
        context['farm'] = farm

        return context


#MEDICATION SUPPLY VIEWS
class MedicationSupplyCreateView(LoginRequiredMixin, CreateView):
    model = MedicationSupply
    form_class = MedicationSupplyForm
    success_url = '/cycle-detail/{cycle_id}'
    template_name = 'production_cycle/medication/create.html'

    def form_valid(self, form):
        form.instance.day = Day.objects.get(id=self.kwargs.get('dayId'))
        return super().form_valid(form)

    
class MedicationSupplyUpdateView(LoginRequiredMixin, UpdateView):
    model = MedicationSupply
    form_class = MedicationSupplyForm
    success_url = '/cycle-detail/{cycle_id}'
    template_name = 'production_cycle/medication/create.html'


class MedicationSupplyDeleteView(LoginRequiredMixin, DeleteView):
    model = MedicationSupply
    success_url = '/cycle-detail/{cycle_id}'


#CYCLE COMPLETED VIEWS
class CycleCompletedCreateView(LoginRequiredMixin, CreateView):
    model = CycleCompleted
    form_class = CycleCompletedForm
    success_url = '/cycle-detail/{cycle_id}'
    template_name = 'production_cycle/medication/create.html'

    def form_valid(self, form):
        form.instance.cycle = Cycle.objects.get(id=self.kwargs.get('cycleId'))
        form.instance.user = self.request.user
        cycle = form.instance.cycle
        cycle.status = 'CLOSED'
        cycle.save()
        return super().form_valid(form)


#SLAUGHTER VIEWS
class SlaughterCreateView(LoginRequiredMixin, CreateView):
    model = Slaughter
    form_class = SlaughterForm
    success_url = '/cycle-detail/{cycle_id}'
    template_name = 'production_cycle/medication/create.html'

    def form_valid(self, form):
        form.instance.cycle = Cycle.objects.get(id=self.kwargs.get('cycleId'))
        return super().form_valid(form)


class SlautherUpdateView(LoginRequiredMixin, UpdateView):
    model = Slaughter
    form_class = SlaughterForm
    success_url = '/cycle-detail/{cycle_id}'
    template_name = 'production_cycle/slaughter/update.html'


class SlaughterListView(LoginRequiredMixin, ListView):
    model = Slaughter
    template_name = 'production_cycle/slaughter/list.html'
    context_object_name = 'slaughters'


class SlaugterDeleteView(DeleteView):
    model = Slaughter
    success_url = '/cycle-detail/{cycle_id}'



#DAY VIEWS
class DayDetailView(LoginRequiredMixin, DetailView):
    model = Day
    template_name = 'production_cycle/day/detail.html'


class DayCreateView(LoginRequiredMixin, CreateView):
    model = Day
    form_class = DayForm
    template_name = 'production_cycle/day/create.html'
    success_url = '/cycle-detail/{cycle_id}'

    def form_valid(self, form):
        form.instance.cycle = Cycle.objects.get(id=self.kwargs.get('cycleId'))
        return super().form_valid(form)


class DayUpdateView(LoginRequiredMixin, UpdateView):
    model = Day
    form_class = DayForm
    template_name = 'production_cycle/day/update.html'
    success_url = '/cycle-detail/{cycle_id}'


class DayDeleteView(LoginRequiredMixin, DeleteView):
    model = Day
    template_name = 'production_cycle/day/delete.html'
    success_url = '/cycle-detail/{cycle_id}'


# FUNCTIONS TO MAKE AND LOAD A FILE WITH STANDARDS
def makeFile():
    if not os.path.exists('static/standards.csv'):
        with open('static/standards.csv', 'w') as file:
            writer = csv.writer(file)
            for standard in Standard.objects.all():
                row = [standard.cycle_day, 
                                standard.average_body_weight, 
                                standard.daily_weight_gain, 
                                standard.average_daily_weight_gain,
                                standard.feed_consumption,
                                standard.cumulative_feed_consumption,
                                standard.water_consumption,
                                standard.cumulative_wather_consumption,
                                standard.feed_conversion]
                writer.writerow(row)
                print(row)

def loadFile():
     with open('static/standards.csv', newline='') as file:
         reader = csv.reader(file)
         for row in reader:
             standard = Standard(cycle_day=row[0], 
                                    average_body_weight=row[1], 
                                    daily_weight_gain=row[2], 
                                    average_daily_weight_gain=row[3],
                                    feed_consumption=row[4],
                                    cumulative_feed_consumption=row[5],
                                    water_consumption=row[6],
                                    cumulative_wather_consumption=row[7],
                                    feed_conversion=row[8])
             standard.save()


#SIGNALS
@receiver(pre_save, sender=MedicationSupply)
def medication_supply_pre_save(sender, instance, **kwargs):
    try:
        instance._pre_save_instance = MedicationSupply.objects.get(pk=instance.pk)
    except MedicationSupply.DoesNotExist:
        instance._pre_save_instance = instance


@receiver(post_save, sender=MedicationSupply)
def update_by_create_medication_supply(sender, instance, created, **kwargs):
    medication = instance.medication
    if created:
        medication.quantity -= instance.quantity
    else:
        pre_save_instance = instance._pre_save_instance
        medication.quantity += pre_save_instance.quantity
        medication.quantity -= instance.quantity

    medication.save()


@receiver(post_delete, sender=MedicationSupply)
def update_by_deleting_medication_supply(sender, instance, **kwargs):
    medication = instance.medication
    medication.quantity += instance.quantity
    medication.save()


@receiver(pre_save, sender=FeedDelivery)
def delivery_pre_save(sender, instance, **kwargs):
    try:
        instance._pre_save_instance = FeedDelivery.objects.get(pk=instance.pk)
    except FeedDelivery.DoesNotExist:
        instance._pre_save_instance = instance

@receiver(post_save, sender=FeedDelivery)
def update_by_create_delivery(sender, instance, created, **kwargs):
    silo = instance.silo
    if created:
        silo.state += instance.quantity * 1000
        silo.feet_type = instance.choices
        
    else: 
        pre_save_instance = instance._pre_save_instance
        silo.state -= pre_save_instance.quantity * 1000
        silo.state += instance.quantity * 1000
        silo.feet_type = instance.choices

    silo.save()


@receiver(pre_delete, sender=Cycle)
def cycle_pre_delete(sender, instance, **kwargs):
    Signal.disconnect(post_delete, receiver=update_by_deleting_day, sender=Day)


@receiver(post_delete, sender=Cycle)
def cycle_post_delete(sender, instance, **kwargs):
    Signal.connect(post_delete, receiver=update_by_deleting_day, sender=Day)


@receiver(post_delete, sender=Day)
def update_by_deleting_day(sender, instance, **kwargs):
    
    cycle = Cycle.objects.get(id=instance.cycle.id)
    cycle.current_herd_size += (instance.deads + instance.selection)
    try:
        silo = cycle.farm.silo_set.get(active=True)
    except Silo.DoesNotExist:
        silo = None
    if silo != None:
        silo.state += instance.total_feed
        silo.save()
    cycle.save()

@receiver(pre_save, sender=Slaughter)
def slaughter_pre_save(sender, instance, **kwargs):
    try:
        instance._pre_save_instance = Slaughter.objects.get(pk=instance.pk)
    except Slaughter.DoesNotExist:
        instance._pre_save_instance = instance

@receiver(post_save, sender=Slaughter)
def update_by_creating_slaughter(sender, instance, created, **kwargs):
    cycle = Cycle.objects.get(id=instance.cycle.id)
    if created:
        cycle.current_herd_size -= instance.quantity
    else:
        pre_save_instance = instance._pre_save_instance
        cycle.current_herd_size += pre_save_instance.quantity
        cycle.current_herd_size -= instance.quantity
    cycle.save()


@receiver(post_delete, sender=Slaughter)
def update_by_deleting_slaughter(sender, instance, **kwargs):
    cycle = Cycle.objects.get(id=instance.cycle.id)
    cycle.current_herd_size += instance.quantity
    cycle.save()

@receiver(pre_save, sender=Day)
def day_pre_save(sender, instance, **kwargs):
    try:
        instance._pre_save_instance = Day.objects.get(pk=instance.pk)
    except Day.DoesNotExist:
        instance._pre_save_instance = instance

@receiver(post_save, sender=Day)
def update_by_creating_day(sender, instance, created, **kwargs):
    cycle = instance.cycle
    farm = cycle.farm
    try:
        silo = Silo.objects.get(active=True, farm=farm)
    except Silo.DoesNotExist:
        silo = None
    if created:
        cycle.current_herd_size -= (instance.deads + instance.selection)
        if silo != None:
            silo.state -= instance.total_feed
    else:
        pre_save_instance = instance._pre_save_instance
        cycle.current_herd_size += (pre_save_instance.deads + pre_save_instance.selection)
        cycle.current_herd_size -= (instance.deads + instance.selection)

        if silo != None:  
            silo.state += pre_save_instance.total_feed
            silo.state -= instance.total_feed
    if silo != None:  
        silo.save()
    cycle.save()
