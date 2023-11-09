from datetime import date

from celery import shared_task
from django.db.models import Q

from staff.models import Staff
from incomes.models import DailyIncome


@shared_task(name="add_income")
def add_income():
    today = date.today()
    staff_ids = Staff.objects.filter(
        Q(end_date__gte=today) | Q(end_date__isnull=True)
    ).values_list("id", flat=True)
    for staff_id in staff_ids:
        DailyIncome.get_or_create(date=today, staff_id=staff_id)
