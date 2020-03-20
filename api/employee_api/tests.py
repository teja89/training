from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Employee, Role
from .serializers import EmployeeSerializer


# tests for views


class TestEmployee(APITestCase):
    client = APIClient()

    @staticmethod
    def add_employee(role="", emp_id=0, first_name="", last_name="", manager_id=0, joining_date=""):
        if emp_id != 0 and first_name != "" and last_name != "" and manager_id != 0 and role and joining_date != "":
            Employee.objects.create(emp_id=emp_id, first_name=first_name, last_name=last_name, manager_id=manager_id,
                                    role=role, joining_date=joining_date)

    @staticmethod
    def add_role(role=""):
        if role != "":
            Role.objects.create(role_name=role)

    def setUp(self):
        # add test data
        self.add_employee(emp_id=1, first_name="Mike", last_name="Spencer", manager_id=1, role=self.add_role("Manager"),
                          joining_date='2010-01-01')
        self.add_employee(emp_id=2, first_name="Micheal", last_name="Jackson", manager_id=1,
                          role=self.add_role("Manager"), joining_date='2011-01-01')
        self.add_employee(emp_id=3, first_name="Mark", last_name="Waugh", manager_id=2, role=self.add_role("Employee"),
                          joining_date='2011-11-01')


class TestGetAllEmployees(TestEmployee):

    def test_get_all_employees(self):
        """
        This test ensures that all employees added in the setUp method
        exist when we make a GET request to the employee/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("employee-list")
        )
        # fetch the data from db
        expected = Employee.objects.all()
        serialized = EmployeeSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_employee_details(self, emp_id=1):
        """
        This test ensures that employees added in the setUp method
        exist when we make a GET request to the employee/:id endpoint
        """
        # hit the API endpoint
        return self.client.get(
            reverse("employee-detail", kwargs={"id": emp_id})
        )
