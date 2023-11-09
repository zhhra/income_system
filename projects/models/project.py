from django.db import models


class Project(models.Model):
    staff = models.ForeignKey(
        "staff.Staff", on_delete=models.CASCADE, related_name="projects"
    )
    date = models.DateField()
    price = models.PositiveBigIntegerField()

    def __str__(self) -> str:
        return f"{self.staff.name} - {self.date}"
