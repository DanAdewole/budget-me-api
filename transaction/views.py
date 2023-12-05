from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from .models import Transaction
from .serializers import TransactionSerializer


@extend_schema(tags=["transaction"])
class CreateTransaction(generics.CreateAPIView):
    """creates a new transaction"""

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data["amount"]
            if amount > 0:
                type = "income"
            else:
                type = "expense"
            serializer.save(user=request.user, type=type)
            response = {
                "message": "Transaction created successfully",
                "status": status.HTTP_201_CREATED,
                "response": serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["transaction"])
class GetTransaction(generics.ListAPIView):
    """gets all transactions"""
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_income = sum(t.amount for t in queryset if t.amount > 0)
        total_expense = sum(t.amount for t in queryset if t.amount < 0)
        balance = float(total_income + total_expense)
        serializer = TransactionSerializer(queryset, many=True)
        response = {
            "message": "Transactions retrieved successfully",
            "status": status.HTTP_200_OK,
            "response": {
                "income": total_income,
                "expense": total_expense,
                "balance": balance,
                "history": serializer.data,
            },
        }
        return Response(response, status=status.HTTP_200_OK)



@extend_schema(tags=["transaction"])
class DeleteTransaction(generics.DestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            transaction_id = self.kwargs['pk']
            return Transaction.objects.get(id=transaction_id, user=self.request.user)
        except Transaction.DoesNotExist:
            return Response({"message": "The transaction does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def perform_destroy(self, instance):
        instance.delete()
