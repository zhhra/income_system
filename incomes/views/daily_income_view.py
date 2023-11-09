import re

from django.db.models import Q
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from staff.models import Staff
from incomes.models import DailyIncome
from incomes.serializers import IncomeSerializer


class DailyIncomeView(GenericAPIView):
    """
    Daily income for each staff.
    """

    serializer_class = IncomeSerializer

    def get_queryset(self):
        queryset = DailyIncome.objects.filter(
            staff_id=self.kwargs["staff_id"]
        ).order_by("-date")
        return queryset

    def get(self, request, staff_id, *args, **kwargs):
        if not Staff.objects.filter(id=staff_id).exists():
            return Response(
                {"error": "Staff not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        date = request.query_params.get("date")
        if date:
            date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
            if not date_pattern.match(date):
                return Response(
                    {"error": "wrong date format"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                obj = self.get_queryset().get(date=date)
            except DailyIncome.DoesNotExist:
                # TODO
                # if Staff.objects.filter(
                #     (Q(end_date__gte=date) | Q(end_date__isnull=True)),
                #     id=staff_id,
                #     start_date__lte=date,
                # ).exists():
                return Response(
                    {"error": "No records were found for this date."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.get_serializer(obj)
        else:
            daily_incomes = self.get_queryset()
            page = self.paginate_queryset(daily_incomes)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(daily_incomes, many=True)
        return Response(serializer.data)
