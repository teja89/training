import get_employee_details as emp
from flask import Response, request, Blueprint, jsonify, abort, make_response
from flask_restful import  Resource
import json

employees = Blueprint('employees',__name__)


class EmployeesApi(Resource):
    def get(self):
        emp_list = emp.get_all_employees_details()
        if emp_list:
            emp_list = json.dumps(emp_list)
            return Response(emp_list, mimetype="application/json", status=200)
        else:
            return Response(json.dumps({"Error":" No employees found"}),mimetype="application/json", status=404 )

    def post(self):
        status = emp.add_new_employee(request)
        status = json.loads(json.dumps(status))
        if status["Error"]:
            return status, 400
        else:
            return status, 200


class EmployeeApi(Resource):
    def get(self, emp_id):
        emp_list = emp.get_employee_details(emp_id)
        if emp_list:
            emp_list = json.dumps(emp_list)
            return Response(emp_list, mimetype="application/json", status=200)
        else:
            return Response(json.dumps({"error":"No employee found"}), mimetype="application/json", status=404)



@employees.route('/api/v1/employees/credit_salary', methods=['PUT'])
def credit_salary():
    if not request.json:
        abort(404)
    status = emp.credit_employee_salary(request)
    try:
        if status["Error"]:
            return status, 400
    except KeyError:
        return jsonify(status)


@employees.route('/api/v1/employees/salary_details/<int:emp_id>/<string:date>', methods=['GET'])
def get_salary_details_by_date(emp_id,date):
    salary_details = emp.get_employee_salary_history_by_date(emp_id,date)
    try:
        if salary_details["Error"]:
            return salary_details, 404
    except KeyError:
        return jsonify(salary_details)

@employees.route('/api/v1/employees/salary_details/<int:emp_id>', methods=['GET'])
def get_salary_details(emp_id):
    salary_details = emp.get_employee_salary_history(emp_id)
    try:
        if salary_details["Error"]:
            return salary_details, 404
    except KeyError:
        return jsonify(salary_details)


@employees.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': 'Not found'}), 404)