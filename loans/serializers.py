from django.shortcuts import get_object_or_404
from rest_framework import serializers

from . import models


class UserCreateSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return models.User.objects.create(name=validated_data.get('user'))


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['name']


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
