from django.forms import ModelForm
from tasks.models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['text', 'farm', 'status', 'important']


class TaskStatus(ModelForm):
    class Meta:
        model = Task
        fields = ['status', ]
