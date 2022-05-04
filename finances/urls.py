from django.urls import path
from .views import FarmFinanceListView, ToAccountTransactionDeleteView, TransactionCreateView, TransactionUpdateView, TransactionDeleteView, ToAccountTransactionCreateView

urlpatterns = [
    path('finances/', FarmFinanceListView.as_view(), name='finances'),
    path('to-account-create-transaction/<int:toAccountId>', ToAccountTransactionCreateView.as_view(), name='createTransaction'),
    path('create-transaction/', TransactionCreateView.as_view(), name='createTransaction'),
    path('update-transaction/<str:pk>', TransactionUpdateView.as_view(), name='updateTransaction'),
    path('delete-transaction/<str:pk>', TransactionDeleteView.as_view(), name='deleteTransaction'),
    path('delete-to-account-transaction/<str:pk>', ToAccountTransactionDeleteView.as_view(), name='deleteToAccountTransaction'),
]