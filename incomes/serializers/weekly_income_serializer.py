from rest_framework import serializers

from staff.models import Staff
from staff.serializers import StaffSerializer


class WeeklyIncomeSerializer(serializers.Serializer):
    staff = serializers.SerializerMethodField()

    def get_staff(self, obj):
        try:
            staff_id = self.context["staff_id"]
            staff = Staff.objects.get(id=staff_id)
        except (Staff.DoesNotExist, KeyError):
            return
        serializer = StaffSerializer(staff)
        return serializer.data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["data"] = instance
        return data
