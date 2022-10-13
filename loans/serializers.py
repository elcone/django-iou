from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from . import models


class UserCreateSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=100)

    def create(self, validated_data):
        try:
            user = models.User.objects.create(name=validated_data.get('user'))
        except IntegrityError:
            raise serializers.ValidationError({
                'name': 'Already existing user name.'
            })

        return user


class UserSerializer(serializers.ModelSerializer):
    owes = serializers.SerializerMethodField()
    owed_by = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = ['name', 'owes', 'owed_by', 'balance']

    def get_owes(self, obj):
        return {
            balance.lender.name: balance.balance
            for balance
            in obj.owes.all()
            if balance.balance > 0.00
        }

    def get_owed_by(self, obj):
        return {
            balance.borrower.name: balance.balance
            for balance
            in obj.owed_by.all()
            if balance.balance > 0.00
        }

    def get_balance(self, obj):
        return obj.balance


class LoanCreateSerializer(serializers.Serializer):
    lender = serializers.CharField(max_length=100)
    borrower = serializers.CharField(max_length=100)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    expiration = serializers.DateTimeField()

    def create(self, validated_data):
        lender = get_object_or_404(models.User,
            name=validated_data.get('lender'))
        borrower = get_object_or_404(models.User,
            name=validated_data.get('borrower'))
        loan_dict = validated_data
        loan_dict['lender'] = lender
        loan_dict['borrower'] = borrower

        return models.Loan.objects.create(**loan_dict)
