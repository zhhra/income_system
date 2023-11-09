from datetime import date, timedelta

from django.db import transaction
from rest_framework import serializers

from staff.models import Staff
from incomes.models import DailyIncome


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = "__all__"

    def update(self, instance, validated_data):
        daily_incomes = []
        start_date = validated_data["start_date"]
        end_date = (
            validated_data["end_date"] if validated_data["end_date"] else date.today()
        )
        all_incomes = DailyIncome.objects.filter(staff_id=instance.id)
        existing_incomes = DailyIncome.objects.filter(
            date__range=(start_date, end_date),
            staff_id=instance.id,
        )
        existing_dates = existing_incomes.values_list("date", flat=True)
        existing_ids = existing_incomes.values_list("id", flat=True)
        while start_date <= end_date and start_date:
            if start_date not in existing_dates:
                daily_incomes.append(DailyIncome(date=start_date, staff=instance))
            start_date += timedelta(days=1)
        try:
            with transaction.atomic():
                obj = super().update(instance, validated_data)
                new_incomes = DailyIncome.objects.bulk_create(daily_incomes)
                new_ids = list(map(lambda i: i.id, new_incomes))
                new_ids.extend(existing_ids)
                all_incomes.exclude(id__in=new_ids).delete()
        except Exception:
            raise serializers.ValidationError("sth went wrong. Please try again later.")
        return obj

    def create(self, validated_data):
        obj = super().create(validated_data)
        daily_incomes = []
        start_date = obj.start_date
        end_date = obj.end_date if obj.end_date else date.today()
        while start_date <= end_date:
            daily_incomes.append(DailyIncome(date=start_date, staff=obj))
            start_date += timedelta(days=1)
        try:
            DailyIncome.objects.bulk_create(daily_incomes)
        except Exception:
            obj.delete()
            raise serializers.ValidationError("sth went wrong. Please try again later.")
        return obj
