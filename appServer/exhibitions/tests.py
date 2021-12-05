import jdatetime
from django.test import TransactionTestCase
from rest_framework import status
from rest_framework.test import APITestCase

import exhibitions
from .models import Exhibition

class ExhibitionDatesTestCase(TransactionTestCase):
    def setUp(self):
        Exhibition.objects.create(
            title="someTestingTitles",
            start_date=jdatetime.date.today(),
            end_date=jdatetime.date.today(),
            address="somewhere around Isfahan Test"
        )

    def test_start_date_is_saved_in_jalali_format(self, *args, **kwargs):
        today = jdatetime.date.today()
        self.assertTrue(Exhibition.objects.filter(start_date=today).exists())
        self.assertTrue(Exhibition.objects.filter(end_date=today).exists())


class VistorAPIsTestCase(APITestCase):
    def setUp(self):
        Exhibition.objects.create(
            title="someTestingTitles",
            start_date=jdatetime.date.today(),
            end_date=jdatetime.date.today(),
            address="somewhere around Isfahan Test"
        )

    def test_visitor_create_with_valid_data(self, *args, **kwargs):
        exhibition = Exhibition.objects.first()
        data = {
         'first_name': "first name",
         'last_name': 'last name',
         'cellphone_number': "09164857984",
         'phone_number': "03145798651",
         'coop_request': 'buy products',
         'product_request': 'microderm probes'
        }
        response = self.client.post(f'/visitor/{exhibition.pk}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        visitor_pk = response.data['id']
        self.assertTrue(exhibition.visitors.filter(pk=visitor_pk).exists())

    def test_visitor_create_with_invalid_exhibition_pk(self, *args, **kwargs):
        data = {
         'first_name': "first name",
         'last_name': 'last name',
         'cellphone_number': "09134879685",
         'phone_number': "03145798651",
         'coop_request': 'buy products',
         'product_request': 'microderm probes'
        }
        response = self.client.post('/visitor/6/', data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_visitor_create_with_invalid_data(self, *args, **kwargs):
        exhibition = Exhibition.objects.first()
        data = {
         'first_name': "first name",
         'last_name': 'last name',
         'cellphone_number': "013879685",
         'phone_number': "31457651",
         'coop_request': ';aksdjlf',
         'product_request': 'sdf probes'
        }
        response = self.client.post(f'/visitor/{exhibition.pk}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

        self.assertIn('cellphone_number', response.data)
        self.assertIn('coop_request', response.data)
        self.assertIn('product_request', response.data)
