from rest_framework import serializers
from django.contrib.auth.models import User
from spending.models import Expense

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","password","email"]
        read_onl_fields=["id"]

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Expense
        fields="__all__"
        read_only_fields=["id","owner","created_at,updated_at"]
        