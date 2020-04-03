import get_details as db
from flask_bcrypt import generate_password_hash, check_password_hash
import re


def get_all_employees_details(emp_id=None):
    manager_list = []
    manager_details= {}
    result = db.get_manager_list(emp_id)

    for manager in result:
        emp_list=[]
        manager_det = get_employee_details(manager[0])
        manager_name = "Manager-" + manager_det["Name"]
        manager_details[manager_name] = manager_det
        result = db.get_employees_list(manager_det["Employee_id"])

        for employee in result:
            employee_list = get_employee_details(employee[0])
            emp_list.append(employee_list)
        manager_details["Employees-Under-"+manager_name] = emp_list

    hr_emp, acc_emp = db.get_all_other_employees()
    if hr_emp:
        manager_details["HR"] = [get_employee_details(emp[0]) for emp in hr_emp]
    if acc_emp:
        manager_details["Accountants"] = [get_employee_details(emp[0]) for emp in acc_emp]

    manager_list.append(manager_details)
    return manager_list


def get_employee_details(emp_id,manager_id=None):
    result, current_holding, salary_history = db.get_employee(emp_id,manager_id)
    if result:
        if result[7]:
            department = result[7].split(",")
        else:
            department = result[6]
        salary_history = format_salary_history(salary_history)
        employee_details = {"Employee_id": result[0], "Name": result[1], "Manager_name": result[2],
                            "Joining_date": result[3], "Role": result[4], "Salary": result[5],
                            "Department": department,"Current_Holding":current_holding,"Salary_History":salary_history}
    else:
        employee_details = {}
    return employee_details


def add_new_employee(request):
    try:
        employee_details = {"first_name": request.json['first_name'], "last_name": request.json['last_name'],
                            "manager_name": request.json['manager_name'], "joining_date": request.json['joining_date'],
                            "role": request.json['role'], "salary": request.json['salary'],
                            "department": request.json['department']}
    except KeyError:
        return {"Error": "Required fields missing in payload"}
    is_data_empty, error, employee_details = verify_data(employee_details)
    if is_data_empty:
        return error

    employee_details["email_id"] = format_email_id(employee_details)
    status = db.add_employee(employee_details)
    return status


def credit_employee_salary(data):

    try:
        db.check_employee(data["emp_id"])
    except Exception:
        return {"Error": "Employee with employee id passed does not exist"}
    if not is_valid_date(data["credited_on"]):
        return {"Error":"Please pass the date in YYYY-MM-DD format"}
    result = db.check_salary_credited(data["emp_id"], data["credited_on"])
    if result:
        status = {"Error": "Salary already credited for the date specified"}

    else:
        status = db.add_salary(data["emp_id"], data)

    return status


def get_employee_salary_history(emp_id):

    try:
        emp_name = db.check_employee(emp_id)
    except Exception:
        return {"Error": "Employee with employee id passed does not exist"}

    salary_history,current_holding = db.get_salary(emp_id)
    salary_history = format_salary_history(salary_history)
    salary_history_details = {"Employee": emp_name, "Current_Holding": current_holding,"Salary_History": salary_history}
    return salary_history_details


def get_employee_salary_history_by_date(emp_id, date, manager_id=None):
    try:
        emp_name = db.check_employee(emp_id)
    except Exception:
        return {"Error": "Employee with employee id passed does not exist"}
    if manager_id:
        if not manager_id == db.is_employee_manager(emp_id):
            return {"Error":"You can view salary details of employees under you"}
    if not is_valid_date(date):
        return {"Error":"Please pass date in YYYY-MM-DD format"}
    salary_history, current_holding = db.get_salary(emp_id, date)
    if salary_history:
        salary_history = format_salary_history(salary_history)
        salary_history_details = {"Employee": emp_name, "Current_Holding": current_holding,"Salary_History": salary_history}
        return salary_history_details
    else:
        return {"Error": "Salary details not found for the date passed"}


def signup(email_id, password):
    try:
        pwd = generate_password_hash(password).decode('utf8')
        status = db.add_new_user(email_id, pwd)
    except ValueError:
        status = {"Error": "Please pass a valid Password"}

    return status


def is_valid_user(email_id, password):
    pwd, emp_id,role, error = db.verify_user_password(email_id, password)
    if emp_id:
        return check_password_hash(pwd, password), emp_id, role, error
    else:
        return False, 0,"", error


def verify_data(employee_details):
    if not str(employee_details["first_name"]).strip():
        return True, {"Error": "First Name cannot be empty"}, {}
    if not str(employee_details["last_name"]).strip():
        return True, {"Error": "Last Name cannot be empty"}, {}
    if not str(employee_details["joining_date"]).strip():
        return True, {"Error": "Joining Date cannot be empty"}, {}
    if not is_valid_date(employee_details["joining_date"]):
        return True, {"Error": "Date should be in YYYY-MM-DD format"}, {}
    if not str(employee_details["role"]).strip():
        return True, {"Error": "Role cannot be empty"}, {}
    if not str(employee_details["manager_name"]).strip():
        if employee_details["role"] != "Manager" and employee_details["role"] != "Accountant" and employee_details[
            "role"] != "HR":
            return True, {"Error": "Manager Name cannot be empty"}, {}
        else:
            employee_details["manager_name"] = "null"
    if int(employee_details["salary"]) <= 0:
        return True, {"Error": "Salary should be greater than 0"}, {}

    if employee_details["role"] == "Employee":
        manager = db.check_manager(employee_details["manager_name"])
        if manager:
            employee_details["manager_name"] = manager[0]
        else:
            return True, {"Error": "Manager name is not valid"}, {}

    role = db.check_role(employee_details["role"])

    if role:
        employee_details["role"] = role[0]
    else:
        return True, {"Error": "Role is not valid"}, {}

    dept = db.check_department(employee_details["department"])

    if dept:
        employee_details["department"] = dept[0]
    else:
        return True, {"Error": "Department name is not valid"}, {}

    if employee_details["role"] == 3 and employee_details["department"] != 1:
        return True, {"Error": "Accountant can only be part of 'Accounts' department"}, {}
    return False, {}, employee_details


def is_valid_date(date):
    reg = "^(19|20)\d\d[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])$"
    pat = re.compile(reg)
    if re.search(pat, date):
        return True
    else:
        return False


def format_email_id(employee_details):
    return str(employee_details["first_name"]).lower() + "." + str(
        employee_details["last_name"]).lower() + "@company.com"


def format_salary_history(salary_history):
    salary_list = [salary for salary in salary_history]
    salary_history = []
    for salary in salary_list:
        salary_dict = {"credited_on": salary[0], "salary_credited": str(salary[2]),
                       "credited_by": salary[1]}
        salary_history.append(salary_dict)
    return salary_history