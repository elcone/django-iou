from django.db.models import F, QuerySet, Sum


class LenderBorrowerQuerySet(QuerySet):
    def get_queryset(self):
        return super().get_queryset().select_related('lender', 'borrower')


class UserQuerySet(QuerySet):
    def with_totals(self):
        return (self
            .prefetch_related(
                'owed_by',
                'owed_by__borrower',
                'owes',
                'owes__lender')
            .annotate(
                total_owed_by=Sum('owed_by__balance'),
                total_owes=Sum('owes__balance'),
                balance=F('total_owed_by')-F('total_owes'))
        )
