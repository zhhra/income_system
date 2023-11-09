from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from staff.models import Staff
from staff.serializers import StaffSerializer
from projects.models import Project
from projects.serializers import ProjectSerializer


class StaffViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for staff.
    """

    http_method_names = ["get", "post", "delete", "put"]
    serializer_class = StaffSerializer
    queryset = Staff.objects.order_by("-id")

    @action(detail=True, methods=["get"])
    def projects(self, request, pk):
        if str(pk).isnumeric():
            projects = Project.objects.filter(staff_id=pk).order_by("-id")
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data)
        return Response(
            {"error": "Not acceptable staff id"},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
