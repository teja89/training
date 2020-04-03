#from app import db as mysql_db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


class Employee(mysql_db.model):
    __tablename__ = 'employee'
    employee_id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    first_name = mysql_db.Column(mysql_db.String(50))
    last_name = mysql_db.Column(mysql_db.String(50))
    manager_id = mysql_db.Column(mysql_db.Integer)
    joining_date = mysql_db.Column(mysql_db.Date)
    role_id = mysql_db.Column(mysql_db.Integer)
    daily_salary = mysql_db.Column(mysql_db.Double)
    department_id = mysql_db.Column(mysql_db.Integer)


class Role(mysql_db.model):
    __tablename__ = 'employee_role'
    id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    role_name = mysql_db.Column(mysql_db.String(50))


class Department(mysql_db.model):
    __tablename__ = 'department'
    department_id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    department_name = mysql_db.Column(mysql_db.String(50))
    department_head = mysql_db.Column(mysql_db.Integer)


class EmployeeSalary(mysql_db.model):
    __tablename__ = 'employee_salary'
    employee_id = mysql_db.Column(mysql_db.Integer)
    current_holding = mysql_db.Column(mysql_db.Double)
    credited_on = mysql_db.Column(mysql_db.Date)
    credited_by = mysql_db.Column(mysql_db.Integer)
    salary_amount = mysql_db.Column(mysql_db.Double)


class Users(mysql_db.model):
    __tablename__ = 'users'
    employee_id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    email_id = mysql_db.Column(mysql_db.String(100))
    password = mysql_db.Column(mysql_db.String(255))
    is_active = mysql_db.Column(mysql_db.String(1))


class EmployeeSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Employee
        sqla_session = mysql_db.session

    employee_id = fields.Number(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    manager_id = fields.Number(required=False)
    joining_date = fields.Date(required=True)
    role_id = fields.Number(required=True)
    daily_salary = fields.Decimal(required=True)
    department_id = fields.Number(required=True)


class RoleSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Role
        sqla_session = mysql_db.session

    id = fields.Number(dump_only=True)
    role_name = fields.String(required=True)


class EmployeeSalarySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = EmployeeSalary
        sqla_session = mysql_db.session

    employee_id = fields.Number(dump_only=True)
    current_holding = fields.Decimal(required=False)
    credited_on = fields.Date(required=True)
    credited_by = fields.Number(required=True)
    salary_amount = fields.Decimal(required=True)


class DepartmentSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Department
        sqla_session = mysql_db.session

    department_id = fields.Number(dump_only=True)
    department_name = fields.String(required=True)
    department_head = fields.Number(required=True)


class UsersSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Users
        sqla_session = mysql_db.session

    employee_id = fields.Number(dump_only=True)
    email_id = fields.String(required=True)
    password = fields.String(required=True)
    is_active = fields.String(required=False)