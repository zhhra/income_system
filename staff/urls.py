from django.urls import include, path
from rest_framework import routers

from staff import views

app_name = "staff"

router = routers.SimpleRouter()
router.register(r"", views.StaffViewSet, basename="staff")

urlpatterns = [
    path("", include(router.urls)),
]
