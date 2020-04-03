import get_employee_details as emp
from flask import Response, request, jsonify, session
from flask_jwt_extended import jwt_required
from flask_restful import Resource
import json


class EmployeesApi(Resource):
    @jwt_required
    def get(self):
        emp_id = None
        if session["role"] not in ["HR", "Manager"]:
            return Response(json.dumps({"Error": "Only Manager or HR can view employee details"}),
                            mimetype="application/json", status=400)
        if session["role"] == "Manager":
            emp_id = session["user_id"]

        emp_list = emp.get_all_employees_details(emp_id)
        if emp_list:
            emp_list = json.dumps(emp_list)
            return Response(emp_list, mimetype="application/json", status=200)
        else:
            return Response(json.dumps({"Error": " No employees found"}), mimetype="application/json", status=404)

    @jwt_required
    def post(self):
        if session["role"] in ["HR", "admin"]:
            status = emp.add_new_employee(request)
            status = json.loads(json.dumps(status))
            try:
                if status["Error"]:
                    return status, 400
            except KeyError:
                return status, 200
        else:
            return {"Error": "Only HR can add new employees"}, 400


class EmployeeApi(Resource):
    @jwt_required
    def get(self, emp_id):
        if session["role"] in ["Employee", "Accountant"] and session["user_id"] == int(emp_id):
            return emp.get_employee_details(emp_id), 200
        elif session["role"] == "HR":
            if emp.get_employee_details(emp_id):
                return emp.get_employee_details(emp_id), 200
            else:
                return {"Error":"Employee with employee id does not exist"},404
        elif session["role"] == "Manager":
            if session["user_id"] == int(emp_id):
                employee_details = emp.get_employee_details(emp_id)
            else:
                employee_details = emp.get_employee_details(emp_id, session["user_id"])
            if employee_details:
                return employee_details, 200
            else:
                return {"Error": "You can view only employees under you."}, 400
        else:
            return {"Error": "You can only view your details"}, 400


class EmployeeSalaryApi(Resource):
    '''
    @jwt_required
    def get(self, emp_id):
        if session["user_id"] == int(emp_id):
            salary_details = emp.get_employee_salary_history(emp_id)
            try:
                if salary_details["Error"]:
                    return salary_details, 404
            except KeyError:
                return jsonify(salary_details)
        else:
            return {"Error": "Employee can view only his salary details"}, 400
    '''
    @jwt_required
    def post(self, emp_id):

        if session["role"] in ["Accountant"]:
            if not request.json:
                return {"Error": "Salary details not passed"}, 400
            try:
                data = {"credited_by": session["user_id"], "emp_id": emp_id, "credited_on": request.json["credited_on"],
                        "salary_amount": request.json["salary_amount"]}
            except KeyError:
                return {"Error": "Required fields for crediting salary missing"}
            status = emp.credit_employee_salary(data)
            try:
                if status["Error"]:
                    return status, 400
            except KeyError:
                return jsonify(status)
        else:
            return {"Error": "Only Accountant can credit salary"},400


class EmployeeSalaryDateApi(Resource):
    @jwt_required
    def get(self, emp_id, date):
        if session["role"] == "HR":
            salary_details = emp.get_employee_salary_history_by_date(emp_id, date)
        elif session["role"] == "Manager":
            manager_id = session["user_id"]
            if manager_id == emp_id:
                salary_details = emp.get_employee_salary_history_by_date(emp_id, date)
            else:
                salary_details = emp.get_employee_salary_history_by_date(emp_id, date, manager_id)
        else:
            if session["user_id"] == emp_id:
                salary_details = emp.get_employee_salary_history_by_date(emp_id, date)
            else:
                return {"Error":"You cannot view other's salary details"}, 400
        try:
            if salary_details["Error"]:
                return salary_details, 404
        except KeyError:
            return jsonify(salary_details)
