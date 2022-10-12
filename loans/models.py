from django.db import models

from . import managers


class User(models.Model):
    name = models.CharField('Name', max_length=100)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['name']

    def __str__(self):
        return self.name


class Loan(models.Model):
    lender = models.ForeignKey(User, on_delete=models.PROTECT,
        related_name='given_loans', verbose_name='Lender')
    borrower = models.ForeignKey(User, on_delete=models.PROTECT,
        related_name='received_loans', verbose_name='Borrower')
    amount = models.DecimalField('Amount', max_digits=12, decimal_places=2)
    expiration = models.DateTimeField('Expiration')

    objects = managers.LenderBorrowerQuerySet.as_manager()

    class Meta:
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'
        ordering = ['expiration']

    def __str__(self):
        return f'{self.lender.name} lend {self.amount:,.2f} to {self.borrower.name}'


class UserBalance(models.Model):
    lender = models.ForeignKey(User, on_delete=models.PROTECT,
        related_name='owed_by', verbose_name='Lender')
    borrower = models.ForeignKey(User, on_delete=models.PROTECT,
        related_name='owes', verbose_name='Borrower')
    balance = models.DecimalField('Amount', max_digits=12, decimal_places=2)

    objects = managers.LenderBorrowerQuerySet.as_manager()

    class Meta:
        verbose_name = 'Balance'
        verbose_name_plural = 'Balances'
        ordering = ['-balance']

    def __str__(self):
        return f'{self.borrower.name} owes {self.balance:,.2f} to {self.lender.name}'
