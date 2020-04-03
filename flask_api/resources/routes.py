from resources.employee import EmployeesApi, EmployeeApi, EmployeeSalaryApi, EmployeeSalaryDateApi
from resources.auth import SignUpApi, LoginApi


def initialize_routes(api):
    api.add_resource(EmployeesApi, '/api/v1/employees')
    api.add_resource(EmployeeApi, '/api/v1/employees/<int:emp_id>')
    api.add_resource(EmployeeSalaryApi, '/api/v1/employees/salary/<int:emp_id>')
    api.add_resource(EmployeeSalaryDateApi, '/api/v1/employees/<int:emp_id>/salary/<date>')
    api.add_resource(SignUpApi, '/api/v1/employees/signup')
    api.add_resource(LoginApi, '/api/v1/employees/login')


