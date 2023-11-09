from rest_framework import viewsets

from incomes.models import DailyIncome
from incomes.serializers import IncomeSerializer


class IncomeViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for incomes.
    """

    http_method_names = ["get", "put"]
    serializer_class = IncomeSerializer
    queryset = DailyIncome.objects.order_by("-id")
