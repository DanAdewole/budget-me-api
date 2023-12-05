from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.shortcuts import get_object_or_404

from .models import Transaction
from .serializers import TransactionSerializer


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


class DeleteTransaction(generics.DestroyAPIView):
    """deletes a transaction"""
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Transaction, id=self.kwargs["pk"])

    def destroy(self, request, *args, **kwargs):
        transaction = self.get_object()
        if transaction.user != request.user:
            response = {
                "message": "You do not have permission to delete this transaction",
                "status": status.HTTP_403_FORBIDDEN,
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(transaction)
        response = {
            "message": "Transaction deleted successfully",
            "status": status.HTTP_204_NO_CONTENT,
        }

    def perform_destroy(self, instance):
        instance.delete()
