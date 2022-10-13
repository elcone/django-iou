import json
from datetime import datetime, timedelta

from django.urls import reverse
from graphene_django.utils.testing import GraphQLTestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from . import models


class UserTests(APITestCase):
    def test_create_user(self):
        url = reverse('create_user')
        response = self.client.post(url, {'user': 'iou'})

        self.assertEqual(response.status_code,
            status.HTTP_201_CREATED,
            'Incorrect status code on user creation')

        self.assertEqual(models.User.objects.count(),
            1,
            'Total users created not correct')

    def test_unique_user_name(self):
        url = reverse('create_user')
        user_name = 'iou'
        response = self.client.post(url, {'user': user_name})
        response = self.client.post(url, {'user': user_name})

        self.assertEqual(response.status_code,
            status.HTTP_400_BAD_REQUEST,
            "Repeated user name shouldn't be allowed")


class LoanTests(APITestCase):
    def test_create_loan(self):
        user_url = reverse('create_user')
        loan_url = reverse('create_loan')

        lender_response = self.client.post(user_url, {'user': 'lender'})
        borrower_response = self.client.post(user_url, {'user': 'borrower'})

        # first loan
        loan_payload = {
            'lender': 'lender',
            'borrower': 'borrower',
            'amount': 100,
            'expiration': datetime.strptime('2022-10-13 13:00:00',
                '%Y-%m-%d %H:%M:%S')
        }
        loan_response = self.client.post(loan_url, loan_payload)
        loan = loan_response.data

        self.assertEqual(loan_response.status_code,
            status.HTTP_201_CREATED,
            'Incorrect status code on loan creation')

        # second loan, now the borrower lends to the lender
        loan_payload = {
            'lender': 'borrower',
            'borrower': 'lender',
            'amount': 80,
            'expiration': datetime.strptime('2022-10-13 13:00:00',
                '%Y-%m-%d %H:%M:%S')
        }
        loan_response = self.client.post(loan_url, loan_payload)
        loan = loan_response.data

        for user in loan.get('users'):
            if user.get('name') == 'lender':
                lender = user
                break
        amount = lender.get('owed_by').get('borrower')
        self.assertEqual(amount, 20.0,
        'IOU not calculated correctly, borrower should owe 20.0 to lender')

        # third loan, non existing user
        loan_payload = {
            'lender': 'lender',
            'borrower': 'non_existing',
            'amount': 100,
            'expiration': datetime.strptime('2022-10-13 13:00:00',
                '%Y-%m-%d %H:%M:%S')
        }
        loan_response = self.client.post(loan_url, loan_payload)
        self.assertEqual(loan_response.status_code, status.HTTP_404_NOT_FOUND,
            "Loans shouldn't be created for not existing users")


class ExpiredLoansTest(GraphQLTestCase):
    GRAPHQL_URL = reverse('expired_loans')

    def test_expired_loan(self):
        user_url = reverse('create_user')
        loan_url = reverse('create_loan')

        lender_response = self.client.post(user_url, {'user': 'lender'})
        borrower_response = self.client.post(user_url, {'user': 'borrower'})

        yesterday = datetime.today() - timedelta(days=1)
        tomorrow = datetime.today() + timedelta(days=1)

        client = APIClient()

        # first loan
        loan_payload = {
            'lender': 'lender',
            'borrower': 'borrower',
            'amount': 100,
            'expiration': yesterday
        }
        loan_response = client.post(loan_url, loan_payload)

        # second loan
        loan_payload = {
            'lender': 'lender',
            'borrower': 'borrower',
            'amount': 100,
            'expiration': yesterday
        }
        loan_response = client.post(loan_url, loan_payload)

        # third loan
        loan_payload = {
            'lender': 'lender',
            'borrower': 'borrower',
            'amount': 100,
            'expiration': tomorrow
        }
        loan_response = client.post(loan_url, loan_payload)

        # expired loans
        response = self.query('''
            query {
                loans {
                    lender {
                        name
                    },
                    borrower {
                        name
                    },
                    amount
                    expiration
                }
            }
            ''')

        content = json.loads(response.content)
        response_loans = len(content.get('data').get('loans'))
        database_loans = models.Loan.objects.filter(
            expiration__lt=datetime.today()).count()
        self.assertEqual(response_loans, database_loans,
            "Incorrect number of expired loans")
