import random
import string
import jdatetime
from django.test import TransactionTestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Exhibition


def random_timedelta():
    number = random.randint(1, 999999)
    return jdatetime.timedelta(days=number)


def random_j_date():
    index = jdatetime.date(year=1377, month=9, day=13)
    timedelta = random_timedelta()
    return index + timedelta


def random_bool():
    number = random.randint(1, 10)
    return True if number % 2 == 0 else False


def random_exhibition():
    return Exhibition.objects.create(
        title=''.join(random.choices(string.ascii_letters, k=20)),
        start_date= random_j_date(),
        end_date=random_j_date(),
        address=''.join(random.choices(string.ascii_letters, k=50)),
        active=random_bool()
    )

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

    def test_visitor_create_with_valid_data_without_options(self, *args, **kwargs):
        exhibition = Exhibition.objects.first()
        data = {
         'first_name': "first name",
         'last_name': 'last name',
         'cellphone_number': "09164857984",
         'phone_number': "03145798651",
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
        }
        response = self.client.post(f'/visitor/{exhibition.pk}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

        self.assertIn('cellphone_number', response.data)
        self.assertIn('coop_request', response.data)
        self.assertIn('product_request', response.data)



class ExhibitionAPITestCase(APITestCase):

    def setUp(self):
        for _ in range(10):
            random_exhibition()

    def test_get_list_of_active_exhibitions(self, *args, **kwargs):
        response = self.client.get("/exhibition/")
        self.assertTrue(response.status_code, status.HTTP_200_OK)

        exhibitions = Exhibition.objects.all()
        active_exhibitions = [item.pk for item in exhibitions.filter(active=True)]
        for item in response.data:
            self.assertIn(item['id'], active_exhibitions)

        deactive_exhibitions = [item.pk for item in exhibitions.filter(active=False)]
        for item in response.data:
            self.assertNotIn(item['id'], deactive_exhibitions)

    def test_if_exhibition_activates_with_a_put_request(self, *args, **kwargs):
        deactive_exhibitions = Exhibition.objects.filter(active=False)
        for item in deactive_exhibitions:
            response = self.client.put(f'/exhibition/{item.pk}/activate/')
            self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
            self.assertTrue(Exhibition.objects.filter(pk=item.pk, active=True).exists())
