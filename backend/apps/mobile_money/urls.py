from django.urls import path
from .views import InitiateTransactionView, TransactionStatusView

urlpatterns = [
    path('initiate/', InitiateTransactionView.as_view(), name='mobile-money-initiate'),
    path('status/<str:reference_id>/', TransactionStatusView.as_view(), name='mobile-money-status'),
]
