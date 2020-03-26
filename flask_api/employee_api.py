from flask import Flask, jsonify, make_response, abort, request
from flask_mysqldb import MySQL
from mysql_conn import get_all_employees_details, get_employee_details, add_new_employee, credit_employee_salary, \
    get_employee_salary_history, get_employee_salary_history_by_date

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'employee'

mysql = MySQL(app)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/api/v1/employees/<int:emp_id>')
def get_employee_details_by_id(emp_id):
    employee_list = get_employee_details(mysql, emp_id)
    if not employee_list:
        abort(404)

    return jsonify(employee_list)


@app.route('/api/v1/employees')
def get_all_employees():
    employees_list = get_all_employees_details(mysql)
    if not employees_list:
        abort(404)
    return jsonify({'employees': employees_list})


@app.route('/api/v1/employees/add_employee', methods=['POST'])
def add_employee():
    if not request.json:
        abort(404)
    status = add_new_employee(mysql, request)
    return jsonify(status)


@app.route('/api/v1/employees/credit_salary/accountant/<int:acc_id>', methods=['PUT'])
def credit_salary(acc_id):
    if not request.json:
        abort(404)
    status = credit_employee_salary(mysql, request, acc_id)
    return jsonify(status)


@app.route('/api/v1/employees/salary_details/<int:emp_id>/<string:date>', methods=['GET'])
def get_salary_details_by_date(emp_id,date):
    salary_details = get_employee_salary_history_by_date(mysql, request, emp_id,date)
    if not salary_details:
        abort(404)
    return jsonify(salary_details)

@app.route('/api/v1/employees/salary_details/<int:emp_id>', methods=['GET'])
def get_salary_details(emp_id):
    salary_details = get_employee_salary_history(mysql, request, emp_id)
    if not salary_details:
        abort(404)
    return jsonify(salary_details)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
