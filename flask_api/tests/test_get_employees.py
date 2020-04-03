import get_details as db

import unittest
import json
from app import app


class BaseTestClass(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app.test_client()

    def tearDown(self) -> None:
        db.drop_all()


class TestEmployees(BaseTestClass):
    def payload(self):
        return json.dumps({
            "first_name": "Henry",
            "last_name": "Olango",
            "manager_name": "",
            "joining_date": "2013-07-11",
            "role": "HR",
            "salary": "1000",
            "department": "HR"
        })

    def error_payload(self):
        missing = json.dumps({
            "first_name": "Henry",
            "last_name": "Olango",
            "manager_name": "",
            "joining_date": "2013-07-11",
            "salary": "1000",
            "department": "HR"
        })
        empty = json.dumps({})
        return missing, empty


    def login(self, email_id, password):
        data = json.dumps({"email_id": email_id, "password": password})
        headers = {"Content-Type": "application/json"}
        response = self.app.post('/api/v1/employees/login', headers=headers, data=data)
        headers = {"Authorization": 'Bearer ' + response.json['token'], "Content-Type": "application/json"}
        return response, headers

    def test_hr_add_employee(self):
        payload = self.payload()
        response, headers = self.login("mike.spencer@company.com", "Ms12345@")
        response = self.app.post('/api/v1/employees', headers=headers, data=payload)
        self.assertEqual(200, response.status_code)

        api_path = '/api/v1/employees/{id}'.format(id=response.json["id"])
        response_get = self.app.get(api_path, headers=headers)
        self.assertEqual(200, response_get.status_code)

    def test_hr_add_employee_data_error(self):
        missing, empty = self.error_payload()
        response, headers = self.login("mike.spencer@company.com", "Ms12345@")
        response = self.app.post('/api/v1/employees', headers=headers, data=missing)
        self.assertEqual(400, response.status_code)
        self.assertEqual("Required fields missing in payload",response.json["Error"])

    def test_employee_add_employee_error(self):
        payload = self.payload()
        response, headers = self.login("rohit.sharma@company.com", "Rs12345@")
        response = self.app.post('/api/v1/employees', headers=headers, data=payload)
        self.assertEqual(400, response.status_code)

    def test_manager_add_employee_error(self):
        payload = self.payload()
        response, headers = self.login("steve.jobs@company.com", "Sj12345@")
        response = self.app.post('/api/v1/employees', headers=headers, data=payload)
        self.assertEqual(400, response.status_code)

    def test_accountant_add_employee_error(self):
        payload = self.payload()
        response, headers = self.login("steve.waugh@company.com", "Sw12345@")
        response = self.app.post('/api/v1/employees', headers=headers, data=payload)
        self.assertEqual(400, response.status_code)

    def test_employee_signup(self):
        data = json.dumps({"email_id": "sachin.tendulkar@company.com", "password": "St12345@"})
        headers = {"Content-Type": "application/json"}
        response = self.app.post('/api/v1/employees/signup', headers=headers, data=data)
        self.assertEqual(200, response.status_code)

    def test_employee_signup_error(self):
        data = json.dumps({"email_id": "sachi.tendulkar@company.com", "password": "St12345@"})
        headers = {"Content-Type": "application/json"}
        response = self.app.post('/api/v1/employees/signup', headers=headers, data=data)
        self.assertEqual(400, response.status_code)

    def test_employee_login(self):
        response, headers = self.login("mike.spencer@company.com", "Ms12345@")
        self.assertEqual(200, response.status_code)

    def test_employee_login_error(self):
        data = json.dumps({"email_id": "mik.spencer@company.com", "password": "Ms12345@"})
        headers = {"Content-Type": "application/json"}
        response = self.app.post('/api/v1/employees/login', headers=headers, data=data)
        self.assertEqual(response.json["Error"], 'No employee found with email id')

    def test_hr_get_all_employees(self):
        response, headers = self.login("mike.spencer@company.com", "Ms12345@")
        response = self.app.get('/api/v1/employees', headers=headers)
        self.assertEqual(200, response.status_code)

    def test_manager_get_employee_under_him(self):
        response, headers = self.login("steve.jobs@company.com", "Sj12345@")
        response = self.app.get('/api/v1/employees', headers=headers)
        self.assertEqual(200, response.status_code)

    def test_accountant_get_all_employees_error(self):
        response, headers = self.login("steve.waugh@company.com", "Sw12345@")
        response = self.app.get('/api/v1/employees', headers=headers)
        self.assertEqual(400, response.status_code)

    def test_employee_get_all_employees_error(self):
        response, headers = self.login("rohit.sharma@company.com", "Rs12345@")
        response = self.app.get('/api/v1/employees', headers=headers)
        self.assertEqual(400, response.status_code)

    def test_hr_get_employee(self):
        response, headers = self.login("mike.spencer@company.com", "Ms12345@")
        response = self.app.get('/api/v1/employees/1', headers=headers)
        self.assertEqual(200, response.status_code)

    def test_hr_get_employee_error(self):
        response, headers = self.login("mike.spencer@company.com", "Ms12345@")
        response = self.app.get('/api/v1/employees/10', headers=headers)
        self.assertEqual(404, response.status_code)
        self.assertEqual("Employee with employee id does not exist", response.json["Error"])

    def test_manager_get_employee(self):
        response, headers = self.login("steve.jobs@company.com", "Sj12345@")
        response = self.app.get('/api/v1/employees/8', headers=headers)
        self.assertEqual(200, response.status_code)

    def test_manager_get_employee_error(self):
        response, headers = self.login("steve.jobs@company.com", "Sj12345@")
        response = self.app.get('/api/v1/employees/1', headers=headers)
        self.assertEqual(400, response.status_code)
        self.assertEqual(response.json["Error"], 'You can view only employees under you.')

    def test_employee_get_self_details(self):
        response, headers = self.login("rohit.sharma@company.com", "Rs12345@")
        response = self.app.get('/api/v1/employees/8', headers=headers)
        self.assertEqual(200, response.status_code)

    def test_employee_get_others_details_error(self):
        response, headers = self.login("rohit.sharma@company.com", "Rs12345@")
        response = self.app.get('/api/v1/employees/1', headers=headers)
        self.assertEqual(400, response.status_code)

    def test_hr_get_employee_salary_by_date(self):
        response, headers = self.login("mike.spencer@company.com", "Ms12345@")
        response = self.app.get('/api/v1/employees/3/salary/2019-12-01', headers=headers)
        self.assertEqual(200, response.status_code)

    def test_hr_get_employee_salary_by_date_error(self):
        response, headers = self.login("mike.spencer@company.com", "Ms12345@")
        response = self.app.get('/api/v1/employees/3/salary/2017-12-01', headers=headers)
        self.assertEqual(404, response.status_code)
        self.assertEqual("Salary details not found for the date passed", response.json["Error"])

    def test_manager_get_employee_salary_by_date(self):
        response, headers = self.login("steve.jobs@company.com", "Sj12345@")
        response = self.app.get('/api/v1/employees/8/salary/2019-12-01', headers=headers)
        self.assertEqual(200, response.status_code)

    def test_manager_get_employee_salary_by_date_error(self):
        response, headers = self.login("steve.jobs@company.com", "Sj12345@")
        response = self.app.get('/api/v1/employees/3/salary/2019-12-01', headers=headers)
        self.assertEqual(404, response.status_code)
        self.assertEqual(response.json["Error"], 'You can view salary details of employees under you')

    def test_accountant_get_employee_salary_by_date(self):
        response, headers = self.login("steve.waugh@company.com", "Sw12345@")
        response = self.app.get('/api/v1/employees/3/salary/2019-12-01', headers=headers)
        self.assertEqual(200, response.status_code)

    def test_employee_get_employee_salary_by_date(self):
        response, headers = self.login("rohit.sharma@company.com", "Rs12345@")
        response = self.app.get('/api/v1/employees/8/salary/2019-12-01', headers=headers)
        self.assertEqual(200, response.status_code)

    def test_employee_get_employee_salary_by_date_error(self):
        response, headers = self.login("rohit.sharma@company.com", "Rs12345@")
        response = self.app.get('/api/v1/employees/3/salary/2019-12-01', headers=headers)
        self.assertEqual(response.json["Error"], "You cannot view other's salary details")
        self.assertEqual(400, response.status_code)

    def test_accountant_credit_salary(self):
        response, headers = self.login("steve.waugh@company.com", "Sw12345@")
        data = json.dumps({"credited_on": "2018-12-02", "salary_amount": "100"})
        response = self.app.post('/api/v1/employees/salary/5', headers=headers, data=data)
        self.assertEqual(200, response.status_code)

    def test_accountant_credit_salary_employee_error(self):
        response, headers = self.login("steve.waugh@company.com", "Sw12345@")
        data = json.dumps({"credited_on": "2018-12-02", "salary_amount": "100"})
        response = self.app.post('/api/v1/employees/salary/15', headers=headers, data=data)
        self.assertEqual(400, response.status_code)
        self.assertEqual("Employee with employee id passed does not exist", response.json["Error"])

    def test_employee_credit_salary_error(self):
        response, headers = self.login("rohit.sharma@company.com", "Rs12345@")
        data = json.dumps({"credited_on": "2018-12-02", "salary_amount": "100"})
        response = self.app.post('/api/v1/employees/salary/5', headers=headers, data=data)
        self.assertEqual(400, response.status_code)

    def test_manager_credit_salary_error(self):
        response, headers = self.login("steve.jobs@company.com", "Sj12345@")
        data = json.dumps({"credited_on": "2018-12-02", "salary_amount": "100"})
        response = self.app.post('/api/v1/employees/salary/5', headers=headers, data=data)
        self.assertEqual(400, response.status_code)

    def test_hr_credit_salary_error(self):
        response, headers = self.login("mike.spencer@company.com", "Ms12345@")
        data = json.dumps({"credited_on": "2018-12-02", "salary_amount": "100"})
        response = self.app.post('/api/v1/employees/salary/5', headers=headers, data=data)
        self.assertEqual(400, response.status_code)

    def test_accountant_credit_salary_same_date_error(self):
        response, headers = self.login("steve.waugh@company.com", "Sw12345@")
        data = json.dumps({"credited_on": "2018-12-02", "salary_amount": "100"})
        response = self.app.post('/api/v1/employees/salary/3', headers=headers, data=data)
        self.assertEqual(400, response.status_code)
        self.assertEqual("Salary already credited for the date specified", response.json["Error"])

    def test_accountant_credit_salary_salary_amount_error(self):
        response, headers = self.login("steve.waugh@company.com", "Sw12345@")
        data = json.dumps({"credited_on": "2012-12-02", "salary_amount": "1000"})
        response = self.app.post('/api/v1/employees/salary/3', headers=headers, data=data)
        self.assertEqual(400, response.status_code)
        self.assertEqual("Salary amount cannot be 0 or greater than the daily salary", response.json["Error"])
