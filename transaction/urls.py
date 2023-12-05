from django.urls import path

from .views import CreateTransaction, GetTransaction, DeleteTransaction

urlpatterns = [
    path("create/", CreateTransaction.as_view(), name="transaction_create"),
    path('history/', GetTransaction.as_view(), name="transaction_history"),
    path('delete/<int:pk>/', DeleteTransaction.as_view(), name='transaction_delete'),
]
