from rest_framework import serializers

from staff.serializers import StaffSerializer
from incomes.models import DailyIncome


class IncomeSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(read_only=True)

    class Meta:
        model = DailyIncome
        fields = ("id", "date", "staff", "total_income", "increase", "decrease")
        read_only_fields = ("date", "total_income")
        extra_kwargs = {
            "increase": {"write_only": True},
            "decrease": {"write_only": True},
        }
