from django.db import models, transaction

from . import managers


class User(models.Model):
    name = models.CharField('Name', max_length=100, unique=True)

    objects = managers.UserQuerySet.as_manager()

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

    @transaction.atomic
    def save(self, *args, **kwargs):
        is_new = False if self.pk else True
        super().save(*args, **kwargs)

        if is_new:
            self.update_balances()

    def update_balances(self):
        lender_balance, lender_is_new = UserBalance.objects.get_or_create(
            lender=self.lender,
            borrower=self.borrower,
            defaults={'balance': self.amount})

        borrower_balance, borrower_is_new = UserBalance.objects.get_or_create(
            lender=self.borrower,
            borrower=self.lender,
            defaults={'balance': 0.0})

        if not lender_is_new:
            if borrower_balance.balance > 0.00 and self.amount >= borrower_balance.balance:
                lender_balance.balance = self.amount - borrower_balance.balance
                borrower_balance.balance = 0

            elif borrower_balance.balance > 0.00 and self.amount < borrower_balance.balance:
                borrower_balance.balance -= self.amount

            else:
                lender_balance.balance += self.amount

            lender_balance.save()
            borrower_balance.save()


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
