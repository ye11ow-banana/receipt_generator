from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from checks.models import Printer, Check


class AddNewOrderViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.url = reverse('checks:add_new_order')
        cls.data = {'order_id': '3333', 'point_id': 1}

    def setUp(self) -> None:
        self.printer1 = Printer.objects.create(
            name='printer1', api_key=1,
            check_type='CLIENT', point_id=1
        )
        self.printer2 = Printer.objects.create(
            name='printer2', api_key=2,
            check_type='KITCHEN', point_id=1
        )

    def test_empty_data_POST(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_printers_at_point_POST(self):
        self.printer1.delete()
        self.printer2.delete()
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_checks_with_order_id_exists_POST(self):
        Check.objects.create(
            printer=self.printer1, type=self.printer1.check_type,
            order=self.data, status='NEW'
        )
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
