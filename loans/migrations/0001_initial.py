# Generated by Django 4.1.2 on 2022-10-12 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='UserBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Amount')),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='owes', to='loans.user', verbose_name='Borrower')),
                ('lender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='owed_by', to='loans.user', verbose_name='Lender')),
            ],
            options={
                'verbose_name': 'Balance',
                'verbose_name_plural': 'Balances',
                'ordering': ['-balance'],
            },
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Amount')),
                ('expiration', models.DateTimeField(verbose_name='Expiration')),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='received_loans', to='loans.user', verbose_name='Borrower')),
                ('lender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='given_loans', to='loans.user', verbose_name='Lender')),
            ],
            options={
                'verbose_name': 'Loan',
                'verbose_name_plural': 'Loans',
                'ordering': ['expiration'],
            },
        ),
    ]
