from rest_framework import generics, permissions
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.response import Response
from rest_framework.views import status


class ListAllEmployeeView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    #permission_classes = [permissions.IsAuthenticated]


class EmployeeDetailView(generics.ListAPIView):
    """
    GET employee/:id/
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            an_employee = self.queryset.get(employee_id=kwargs["id"])
            return Response(EmployeeSerializer(an_employee).data)
        except Employee.DoesNotExist:
            return Response(
                data={
                    "message": "Employee with id: {} does not exist".format(kwargs["id"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
