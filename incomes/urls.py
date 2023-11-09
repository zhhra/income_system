from django.urls import include, path
from rest_framework import routers

from incomes import views

app_name = "incomes"


router = routers.SimpleRouter()
router.register(r"", views.IncomeViewSet, basename="incomes")

urlpatterns = [
    path(
        "<int:staff_id>/daily/",
        views.DailyIncomeView.as_view(),
        name="daily_income",
    ),
    path(
        "<int:staff_id>/weekly/",
        views.WeeklyIncomeView.as_view(),
        name="weekly_income",
    ),
    path("", include(router.urls)),
]
