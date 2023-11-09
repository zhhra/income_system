from rest_framework import viewsets

from projects.models import Project
from projects.serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for projects.
    """

    http_method_names = ["get", "post"]
    serializer_class = ProjectSerializer
    queryset = Project.objects.order_by("-id")
