from django.urls import include, path
from rest_framework import routers

from projects import views

app_name = "projects"

router = routers.SimpleRouter()
router.register(r"", views.ProjectViewSet, basename="projects")

urlpatterns = [
    path("", include(router.urls)),
]
