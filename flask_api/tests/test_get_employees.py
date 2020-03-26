
import unittest
import json
from app import app


class BaseTestClass(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app.test_client()


class TestEmployees(BaseTestClass):
    def test_get_all_employees(self):
        response = self.app.get('/api/v1/employees')
        self.assertEqual(200, response.status_code)

    def test_get_employee(self):
        response = self.app.get('/api/v1/employees/4')
        self.assertEqual(200, response.status_code)

    def test_get_employee_error(self):
        response = self.app.get('/api/v1/employees/10')
        self.assertEqual(404, response.status_code)

    def test_add_employee(self):
        payload = json.dumps({
            "first_name": "Henry",
            "last_name": "Olango",
            "manager_id": "14",
            "joining_date": "2013-07-11",
            "role": "Accountant",
            "salary": "1000",
            "department_id": "1"
        })

        response = self.app.post('/api/v1/employees',headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(200, response.status_code)

        api_path = '/api/v1/employees/{id}'.format(id=response.json["id"])
        response_get = self.app.get(api_path)
        self.assertEqual(200,response_get.status_code)

    def test_add_employee_error(self):
        payload = json.dumps({
            "first_name": "Sachin",
            "last_name": "Tendulkar",
            "manager_id": "2",
            "role": "Accountant",
            "salary": "1000",
            "department_id": "1"
        })
        response = self.app.post('/api/v1/employees', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(400, response.status_code)
        self.assertEqual("Required fields missing in payload",response.json["Error"])

    def test_credit_salary(self):
        payload = json.dumps({
            "accountant_id": "6",
            "credited_on": "2013-07-22",
            "employee_id": "14",
            "salary_amount": 500
        })

        response = self.app.put('/api/v1/employees/credit_salary',headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(200, response.status_code)

        api_path = '/api/v1/employees/salary_details/{id}/{credited_date}'.format(id=response.json["id"],credited_date='2013-07-11')
        response_get = self.app.get(api_path)
        self.assertEqual(200,response_get.status_code)

    def test_credit_salary_accountant_error(self):
        payload = json.dumps({
            "accountant_id": "1",
            "credited_on": "2013-07-11",
            "employee_id": "14",
            "salary_amount": 500
        })
        response = self.app.put('/api/v1/employees/credit_salary', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(400, response.status_code)
        self.assertEqual("Account ID submitted is not an accountant. Only Accountants can credit salary", response.json["Error"])

    def test_credit_salary_date_error(self):
        payload = json.dumps({
            "accountant_id": "6",
            "credited_on": "2012-09-15",
            "employee_id": "2",
            "salary_amount": 500
        })
        response = self.app.put('/api/v1/employees/credit_salary', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(400, response.status_code)
        self.assertEqual("Salary already credited for the date specified",response.json["Error"])

    def test_credit_salary_amount_error(self):
        payload = json.dumps({
            "accountant_id": "6",
            "credited_on": "2012-09-13",
            "employee_id": "2",
            "salary_amount": 600
        })
        response = self.app.put('/api/v1/employees/credit_salary', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(400, response.status_code)
        self.assertEqual("Salary amount cannot be 0 or greater than the daily salary",response.json["Error"])

    def test_credit_salary_employee_error(self):
        payload = json.dumps({
            "accountant_id": "6",
            "credited_on": "2012-09-13",
            "employee_id": "10",
            "salary_amount": "600"
        })
        response = self.app.put('/api/v1/employees/credit_salary', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(400, response.status_code)
        self.assertEqual("Employee with employee id passed does not exist",response.json["Error"])


    def test_get_salary_history(self):
        response = self.app.get('/api/v1/employees/salary_details/2')
        self.assertEqual(200,response.status_code)

    def test_get_salary_history_error(self):
        response = self.app.get('/api/v1/employees/salary_details/10')
        self.assertEqual(404, response.status_code)

    def test_get_salary_history_date(self):
        response = self.app.get('/api/v1/employees/salary_details/2/2012-09-15')
        self.assertEqual(200,response.status_code)

    def test_get_salary_history_date_error(self):
        response = self.app.get('/api/v1/employees/salary_details/2/2015-02-03')
        self.assertEqual(404, response.status_code)
        self.assertEqual("Salary details not found for the date passed", response.json["Error"])

    def test_get_salary_history_date_employee_error(self):
        response = self.app.get('/api/v1/employees/salary_details/10/2015-02-03')
        self.assertEqual(404, response.status_code)
        self.assertEqual("Employee with employee id passed does not exist", response.json["Error"])
