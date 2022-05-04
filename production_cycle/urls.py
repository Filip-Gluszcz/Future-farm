from django.urls import path
from production_cycle import views
from account import views as account_views

urlpatterns = [
    path('create-cycle/<int:id>/', views.CycleCreateView.as_view(), name='createCycle'),
    path('cycle-detail/<str:pk>/', views.CycleDetailView.as_view(), name='cycleDetail'),
    path('delete-cycle/<str:pk>/', views.CycleDeleteView.as_view(), name='deleteCycle'),
    path('update-cycle/<str:pk>/',views.CycleUpdateView.as_view(), name='updateCycle'),

    path('create-slaugter/<int:cycleId>/', views.SlaughterCreateView.as_view(), name='createSlaughter'),
    path('update-slaugter/<str:pk>', views.SlautherUpdateView.as_view(), name='updateSlaughter'),
    path('delete-slaugter/<str:pk>', views.SlaugterDeleteView.as_view(), name='deleteSlaughter'),

    path('create-feed-delivery/<int:farmId>/<int:cycleId>/', views.FeedDeliveryCreateView.as_view(), name='createFeedDelivery'),
    path('update-feed-delivery/<int:farmId>/<str:pk>', views.FeedDeliveryUpdateView.as_view(), name='updateFeedDelivery'),
    path('detail-feed-delivery/<str:pk>', views.FeedDeliveryDetailView.as_view(), name='detailFeedDelivery'),
    path('delete-feed-delivery/<str:pk>/<int:farmId>', views.FeedDeliveryDeleteView.as_view(), name='deleteFeedDelivery'),
    
    path('create-stored-feed/<int:farmId>/<int:siloId>/', views.StoredFeedCreateView.as_view(), name='createStoredFeed'),
    path('restore-feed/<int:farmId>/', views.RestoreFeedView.as_view(), name='restoreFeed'),
    path('update-stored-feed/<int:farmId>/<str:pk>', views.StoredFeedUpdateView.as_view(), name='updateStoredFeed'),
    path('delete-stored-feed/<int:farmId>/<str:pk>', views.StoredFeedDeleteView.as_view(), name='deleteStoredFeed'),

    path('medications/<int:farmId>/', views.MedicationListView.as_view(), name='medications'),
    path('create-medication/<int:farmId>', views.MedicationCreateView.as_view(), name='createMedication'),
    path('update-medication/<str:pk>', views.MedicationUpdateView.as_view(), name='updateMedication'),
    path('delete-medication/<str:pk>', views.MedicationDeleteView.as_view(), name='deleteMedication'),

    path('create-medication-supply/<int:dayId>', views.MedicationSupplyCreateView.as_view(), name='createMedicationSupply'),
    path('update-medication-supply/<str:pk>', views.MedicationSupplyUpdateView.as_view(), name='updateMedicationSupply'),
    path('delete-medication-supply/<str:pk>', views.MedicationSupplyDeleteView.as_view(), name='deleteMedicationSupply'),

    path('create-cycle-completed/<int:cycleId>', views.CycleCompletedCreateView.as_view(), name='createCycleCompleted'),

    path('create-day/<int:cycleId>/', views.DayCreateView.as_view(), name='createDay'),
    path('update-day/<str:pk>', views.DayUpdateView.as_view(), name='updateDay'),
    path('detail-day/<str:pk>', views.DayDetailView.as_view(), name='detailDay'),
    path('delete-day/<str:pk>', views.DayDeleteView.as_view(), name='deleteDay')
]

# <int:farmId>/