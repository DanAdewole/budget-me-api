from django.db import models
from django.contrib.auth.models import User


TRANSACTION_TYPES = (
    ("income", "income"),
    ("expense", "expense"),
)


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, default="income")

    class Meta:
        ordering = ["-date_added"]

    def __str__(self):
        return self.description
