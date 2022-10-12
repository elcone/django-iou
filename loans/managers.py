from django.db.models import QuerySet


class LenderBorrowerQuerySet(QuerySet):
    def get_queryset(self):
        return super().get_queryset().select_related('lender', 'borrower')
