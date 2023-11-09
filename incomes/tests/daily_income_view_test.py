from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from staff.models import Staff
from incomes.models import DailyIncome
from incomes.serializers import IncomeSerializer


class DailyIncomeViewTestCase(TestCase):
    def setUp(self):
        self.staff = Staff.objects.create(name="Test Staff", start_date="2023-09-20")
        self.income1 = DailyIncome.objects.create(
            staff=self.staff, date="2023-09-22", total_income=1049
        )
        self.income2 = DailyIncome.objects.create(
            staff=self.staff, date="2023-09-21", total_income=1049
        )
        self.incomes = DailyIncome.objects.filter(staff=self.staff)

    def test_get_single_income(self):
        # Test getting a single income record by date
        url = reverse("incomes:daily_income", kwargs={"staff_id": self.staff.id})
        response = self.client.get(url, {"date": "2023-09-22"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, IncomeSerializer(self.income1).data)

    def test_get_multiple_incomes(self):
        # Test getting multiple income records for a staff
        url = reverse("incomes:daily_income", kwargs={"staff_id": self.staff.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO below
        # self.assertEqual(
        #     response.data,
        #     IncomeSerializer(self.incomes, many=True).data,
        # )

    def test_staff_not_found(self):
        # Test case where the staff does not exist
        url = reverse("incomes:daily_income", kwargs={"staff_id": 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Staff not found"})

    def test_no_incomes_for_date(self):
        # Test case where no incomes found for a specific date
        url = reverse("incomes:daily_income", kwargs={"staff_id": self.staff.id})
        response = self.client.get(url, {"date": "2023-09-20"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {"error": "No records were found for this date."}
        )

    def test_date_wrong_format(self):
        # Test case where date format is wrong
        url = reverse("incomes:daily_income", kwargs={"staff_id": self.staff.id})
        response = self.client.get(url, {"date": "2023-09-2"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "wrong date format"})
