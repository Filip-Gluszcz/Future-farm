from django.urls import path
from tasks import views

urlpatterns = [
    path('tasks/', views.TaskListView.as_view(), name='tasks'),
    path('update-task-status/<str:pk>/', views.TaskChangeStatus.as_view(),
         name='updateTaskStatus'),
    path('update-task/<str:pk>/', views.TaskUpdateView.as_view(),
         name='updateTask'),
    path('create-task/', views.TaskCreateView.as_view(), name='createTask'),
]
