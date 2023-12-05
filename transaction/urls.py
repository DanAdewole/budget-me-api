from django.urls import path

from .views import CreateTransaction, GetTransaction, RetrieveEditDestroyTransaction

urlpatterns = [
    path("create/", CreateTransaction.as_view(), name="transaction_create"),
    path("history/", GetTransaction.as_view(), name="transaction_history"),
    path(
        "<int:pk>/", RetrieveEditDestroyTransaction.as_view(), name="transaction_delete"
    ),
]
