from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from tasks.models import Task
from account.models import Farm
from tasks.forms import TaskForm, TaskStatus


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/create.html'
    success_url = '/tasks/'
    form_class = TaskForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = '/tasks/'


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    context_object_name = 'task'
    success_url = '/tasks/'
    form_class = TaskForm


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['farms'] = Farm.objects.filter(user=self.request.user.id)
        context['tasks'] = Task.objects.filter(user=self.request.user.id)
        context['userFullName'] = self.request.user.get_full_name()
        return context


class TaskChangeStatus(LoginRequiredMixin, UpdateView):
    model = Task
    success_url = '/tasks/'
    form_class = TaskStatus
