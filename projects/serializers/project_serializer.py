from datetime import date

from django.db import transaction
from django.db.utils import DataError
from rest_framework import serializers

from incomes.models import DailyIncome
from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ("date",)

    def create(self, validated_data):
        validated_data["date"] = date.today()
        try:
            with transaction.atomic():
                obj = super().create(validated_data)
                DailyIncome.objects.get_or_create(staff=obj.staff, date=obj.date)[
                    0
                ].save()
        except DataError:
            raise serializers.ValidationError(
                "The entered price is too big. Please contact the support team."
            )
        return obj
