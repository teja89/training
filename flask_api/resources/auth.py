
from flask_restful import Resource
import get_employee_details as emp
import re
from flask import request, session
from flask_jwt_extended import create_access_token
import datetime


class SignUpApi(Resource):
    def post(self):
        if request.json:
            try:
                email_id = request.json["email_id"]
                password = request.json["password"]
                if not is_valid_email(email_id):
                    return {"Error": "Email Id should be company email id"}, 400

                if not is_valid_password(password):
                    return {"Error": "Password should have min. 8 characters with 1 uppercase and 1 lowercase and 1 "
                                     "symbol"}, 400
                status = emp.signup(email_id, password)

            except (KeyError, TypeError) as e:
                print(e)
                status = {"Error": "Please pass both Email Id and Password"}
                return status, 400
        else:
            status = {"Error": "Please pass both Email Id and Password"}
            return status, 400

        try:
            if status["Error"]:
                return status, 400
        except KeyError:
            return status, 200


class LoginApi(Resource):
    def post(self):
        try:
            email_id = request.json["email_id"]
            password = request.json["password"]
            if not is_admin(email_id,password):
                authorized, emp_id,role, error = emp.is_valid_user(email_id,password)
                if not authorized:
                    return error, 401
                else:
                    session["user_id"] = emp_id
                    session["role"] = role
            else:
                emp_id = 0
                session["user_id"] = emp_id
                session["role"] = "admin"
        except KeyError:
            return {"Error": "Please pass both Email Id and Password"}

        expires = datetime.timedelta(days=1,minutes=5)
        access_token = create_access_token(identity=str(emp_id), expires_delta=expires)
        return {'token': access_token}, 200


def is_valid_email(email_id):

    if re.search('@company.com', email_id) :
        return True
    else:
        return False


def is_valid_password(password):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
    pat = re.compile(reg)
    if re.search(pat, password):
        return True
    else:
        return False


def is_admin(email_id,password):
    if email_id == 'admin@company.com' and password == 'admin':
        return True
    else:
        return False