from datetime import datetime

import graphene
from graphene_django import DjangoObjectType

from . import models


class UserType(DjangoObjectType):
    class Meta:
        model = models.User
        fields = ['name']


class LoanType(DjangoObjectType):
    class Meta:
        model = models.Loan
        fields = ['lender', 'borrower', 'amount', 'expiration']


class Query(graphene.ObjectType):
    loans = graphene.List(LoanType)

    def resolve_loans(root, info):
        return (models
            .Loan
            .objects
            .select_related('lender', 'borrower')
            .filter(expiration__lt=datetime.today()))


schema = graphene.Schema(query=Query)
