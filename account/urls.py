from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls.base import reverse_lazy
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', LoginView.as_view(redirect_field_name='/farm-list/',template_name='account/profile/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),

    path('register/', views.UserRegistration.as_view(), name='register'),
    path('account/', views.AccountDetailView.as_view(), name='account'),

    path('reset_password/',
     PasswordResetView.as_view(template_name="account/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        PasswordResetDoneView.as_view(template_name="account/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     PasswordResetConfirmView.as_view(template_name="account/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        PasswordResetCompleteView.as_view(template_name="account/password_reset_done.html"), 
        name="password_reset_complete"),
   
    
    path('update-user/<str:pk>', views.UserUpdateView.as_view(), name='updateUser'),
    path('update-profile/<str:pk>', views.ProfileUpdateView.as_view(), name='updateProfile'),
    path('create-profile/', views.ProfileCreateView.as_view(), name='createProfile'),
    
    path('create-farm/', views.FarmCreateView.as_view(), name='createFarm'),
    path('update-farm/<str:pk>', views.FarmUpdateView.as_view(), name='updateFarm'),
    path('delete-farm/<str:pk>', views.FarmDeleteView.as_view(), name='deleteFarm'),
    path('farm-list/', views.FarmListView.as_view(), name='farmList'),
    
    path('create-silo/', views.SiloCreateView.as_view(), name='createSilo'),
    path('update-silo/<str:pk>', views.SiloUpdateView.as_view(), name='updateSilo'),
    path('delete-silo/<str:pk>', views.SiloDeleteView.as_view(), name='deleteSilo'),
    path('silos/<int:farmId>', views.SiloListView.as_view(), name='silos'),
    
    path('silo-activate/<int:farmId>/<str:pk>', views.SiloActivateView.as_view(), name='siloActivate'),
    path('silo-deactivate/<int:farmId>/<str:pk>', views.SiloDeactivateView.as_view(), name='siloDeactivate'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
