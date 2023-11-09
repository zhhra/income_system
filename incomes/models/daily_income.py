from django.db import models
from django.db.models import Sum

from projects.models import Project


class DailyIncome(models.Model):
    staff = models.ForeignKey(
        "staff.Staff", on_delete=models.CASCADE, related_name="daily_incomes"
    )
    date = models.DateField()
    increase = models.PositiveBigIntegerField(default=0)
    decrease = models.PositiveBigIntegerField(default=0)
    total_income = models.PositiveBigIntegerField(default=0)

    class Meta:
        unique_together = ("staff", "date")
        indexes = [
            models.Index(
                fields=[
                    "staff_id",
                ]
            ),
            models.Index(
                fields=[
                    "date",
                ]
            ),
        ]

    def __str__(self) -> str:
        return f"{self.staff.name} - {self.date}"

    def save(self, *args, **kwargs):
        projects_income = Project.objects.filter(
            date=self.date, staff=self.staff
        ).aggregate(income=Sum("price"))["income"]
        if projects_income is None:
            projects_income = 0
        self.total_income = projects_income + self.increase - self.decrease
        return super().save(*args, **kwargs)
