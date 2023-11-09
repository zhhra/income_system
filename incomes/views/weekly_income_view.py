import re
from datetime import datetime, timedelta

from django.db.models import F, Func, IntegerField, QuerySet, Sum
from django.db.models.functions import Floor
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from incomes.models import DailyIncome
from incomes.serializers import WeeklyIncomeSerializer


class DateDiff(Func):
    function = "DATEDIFF"
    output_field = IntegerField()


class WeeklyIncomeView(GenericAPIView):
    """
    Weekly income for each staff.
    """

    serializer_class = WeeklyIncomeSerializer

    def get_queryset(self):
        queryset = DailyIncome.objects.filter(staff_id=self.kwargs["staff_id"])
        return queryset

    def get(self, request, staff_id, *args, **kwargs):
        try:
            from_date_param = request.query_params["from_date"]
            to_date_param = request.query_params["to_date"]
        except KeyError:
            return Response(
                {"error": "start and end dates are mandatory."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if not (
            date_pattern.match(from_date_param) and date_pattern.match(to_date_param)
        ):
            return Response(
                {"error": "Invalid date format."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from_date = datetime.strptime(from_date_param, "%Y-%m-%d")
        to_date = datetime.strptime(to_date_param, "%Y-%m-%d")
        diff_from_saturday = 5 - from_date.weekday()
        if diff_from_saturday < 0:
            diff_from_saturday += 7
        first_saturday = from_date + timedelta(days=diff_from_saturday)
        last_saturday = first_saturday
        while last_saturday <= to_date:
            last_saturday += timedelta(days=7)

        if first_saturday and last_saturday:
            queryset = (
                self.get_queryset()
                .filter(date__range=(first_saturday, last_saturday))
                .annotate(week_num=Floor(DateDiff(F("date"), first_saturday) / 7))
                .values("week_num")
                .annotate(total_income=Sum("total_income"))
            )
            for item in queryset:
                item["start_date"] = (
                    first_saturday + timedelta(item["week_num"] * 7)
                ).date()
        else:
            queryset = QuerySet()
        serializer = self.get_serializer(queryset, context={"staff_id": staff_id})
        return Response(serializer.data)
