from resources.employee import EmployeesApi, EmployeeApi


def initialize_routes(api):
    api.add_resource(EmployeesApi, '/api/v1/employees')
    api.add_resource(EmployeeApi, '/api/v1/employees/<emp_id>')