def get_all_employees_details(mysql):
    cur = mysql.connection.cursor()
    cur.execute("""
                    SELECT e.employee_id,concat(e.first_name," ",e.last_name) as emp_name,concat(m.first_name," ",m.last_name) as manager_name,cast(e.joining_date as char),r.role_name,coalesce(e.daily_salary,'NA') as daily_salary,d.department_name 
                    FROM employee.employee e
                    inner join employee.employee_role r on r.id = e.role_id 
                    inner join employee.department d on d.department_id = e.department_id
                    inner join employee.employee m on m.employee_id = e.manager_id
                    where r.id != 2;
                """)
    result = cur.fetchall()
    emp_list = []
    for employee in result:
        employee_list = {"Employee_id": employee[0], "Name": employee[1], "Manager_name": employee[2],
                         "Joining_date": employee[3], "Role": employee[4], "Salary": employee[5],
                         "Department": employee[6]}
        emp_list.append(employee_list)

    cur.execute("""
                        SELECT e.employee_id,concat(e.first_name," ",e.last_name) as emp_name,concat(m.first_name," ",m.last_name) as manager_name,cast(e.joining_date as char),r.role_name,coalesce(e.daily_salary,'NA') as daily_salary, a.departments
                        FROM employee.employee e
                        inner join employee.employee_role r on r.id = e.role_id 
                        inner join (select d.department_head ,group_concat(d.department_name separator ', ') as departments
                        from employee.department d
                        group by d.department_head) a on a.department_head = e.employee_id
                        inner join employee.employee m on m.employee_id = e.manager_id
                        where r.id = 2;
                    """)
    result = cur.fetchall()
    for manager in result:
        manager_list = {"Employee_id": manager[0], "Name": manager[1], "Manager_name": manager[2],
                        "Joining_date": manager[3], "Role": manager[4], "Salary": manager[5],
                        "Department": manager[6].split(',')}
        emp_list.append(manager_list)
    return emp_list


def get_employee_details(mysql, emp_id):
    cur = mysql.connection.cursor()
    cur.execute("""
                    SELECT e.employee_id,concat(e.first_name," ",e.last_name) as name,concat(m.first_name," ",m.last_name) as manager_name,cast(e.joining_date as char) as date,r.role_name,coalesce(e.daily_salary,'NA'),d.department_name, coalesce(a.departments,"") departments
                    FROM employee.employee e
                    inner join employee.employee_role r on r.id = e.role_id
                    inner join employee.department d on d.department_id = e.department_id
                    left join (select d.department_head ,group_concat(d.department_name separator ', ') as departments
                        from employee.department d
                        group by d.department_head) a on a.department_head = e.employee_id
                    inner join employee.employee m on m.employee_id = e.manager_id 
                    where
                    e.employee_id = {employee_id};
                """.format(employee_id=emp_id))
    result = cur.fetchone()
    if result:
        if result[7]:
            department = result[7].split(",")
        else:
            department = result[6]
        employee_details = {"Employee_id": result[0], "Name": result[1], "Manager_name": result[2],
                    "Joining_date": result[3], "Role": result[4], "Salary": result[5],
                    "Department": department}
    else:
        employee_details ={}
    return employee_details


def add_new_employee(mysql, request):
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    manager_id = request.json['manager_id']
    joining_date = request.json['joining_date']
    role = request.json['role']
    salary = request.json['salary']
    department_id = request.json['department_id']
    cur = mysql.connection.cursor()
    cur.execute("""select id from employee.employee_role where role_name = '{role}';""".format(role=role))
    role = cur.fetchone()[0]
    if role == 3 and department_id != 1:
        return {"Error": "Accountant can only be part of 'Accounts' department"}
    cur.execute(
        "insert into employee.employee(first_name,last_name,manager_id,joining_date,role_id,department_id) values('{first_name}','{last_name}',{manager_id},'{joining_date}',{role},{department});".format(
            first_name=first_name, last_name=last_name, manager_id=manager_id, joining_date=joining_date, role=role,
            department=department_id))
    cur.execute('commit;')
    cur.execute('select max(employee_id) from employee.employee ;')
    emp_id = cur.fetchone()[0]
    cur.execute(
        'insert into employee.employee_salary values({emp_id},{salary},0,null);'.format(emp_id=emp_id, salary=salary))
    cur.execute('commit;')
    return {"status": "Employee added"}


def credit_employee_salary(mysql, request, acc_id):
    cur = mysql.connection.cursor()
    cur.execute("""select r.role_name
                    from employee.employee e 
                    inner join employee.employee_role r on r.id = e.role_id
                    where
                    e.employee_id ={emp_id}; """.format(emp_id=acc_id))

    role = cur.fetchone()[0]
    if role.lower() != 'accountant':
        status = {"status": "Employee Id submitted is not an accountant. Only Accountants can credit salary"}
        return status
    credited_on = request.json["credited_on"]
    emp_id = request.json["employee_id"]
    salary_amount = request.json["salary_amount"]
    cur.execute(""" select s.current_holding
                    from employee.employee_salary s 
                    inner join employee.employee e on e.employee_id = s.employee_id
                    where 
                    s.employee_id = {emp_id} 
                    and s.credited_on >= e.joining_date
                    and s.credited_on = '{credited_on}'
                    and s.credited_on is not null""".format(emp_id=emp_id, credited_on=credited_on))
    result = cur.fetchone()
    if result:
        status = {"Error": "Salary already credited for the date specified"}

    else:
        cur.execute(""" select coalesce(sum(salary_amount),0)
                        from employee.employee_salary s
                        where
                        s.employee_id = {employee_id}""".format(employee_id=emp_id))
        result = cur.fetchone()[0]
        current_holding = float(result) + salary_amount
        cur.execute(""" select e.daily_salary from employee.employee e where e.employee_id = {employee_id}""".format(
            employee_id=emp_id))
        daily_salary = cur.fetchone()[0]
        if 0 < salary_amount <= daily_salary:
            cur.execute(""" insert into employee.employee_salary values({employee_id},{current_holding},'{credited_on}',
                                                                    {credited_by},{salary_amount})
                        ;""".format(current_holding=current_holding, employee_id=emp_id, credited_on=credited_on,
                                    credited_by=acc_id, salary_amount=salary_amount))
            cur.execute('commit;')
            status = {"status": "Salary Credited"}
        else:
            status = {"status": "Salary amount cannot be 0 or greater than the daily salary"}

    return status


def get_employee_salary_history(mysql, request, emp_id):
    cur = mysql.connection.cursor()
    cur.execute("""select concat(e.first_name," ",e.last_name) as employee_name from employee.employee e where 
                    e.employee_id = {emp_id}""".format(emp_id=emp_id))
    emp_name = cur.fetchone()[0]
    cur.execute(""" select s.current_holding,cast(s.credited_on as char),s.salary_amount,coalesce(concat(e.first_name," ",e.last_name),"NA") as accountant  from employee.employee_salary s
                left join employee.employee e on e.employee_id = s.credited_by
                where s.employee_id ={emp_id}
                order by credited_on desc;""".format(emp_id=emp_id))
    salary_history = cur.fetchall()
    salary_list = [salary for salary in salary_history]
    print(salary_list)
    salary_history = []
    for salary in salary_list:
        salary_dict = {"current_holding": salary[0], "credited_on": salary[1], "salary_credited": str(salary[2]),
                       "credited_by": salary[3]}
        salary_history.append(salary_dict)
    salary_history_details = {"Employee": emp_name, "Salary_History": salary_history}
    return salary_history_details


def get_employee_salary_history_by_date(mysql, request, emp_id, date):
    cur = mysql.connection.cursor()
    cur.execute("""select concat(e.first_name," ",e.last_name) as employee_name from employee.employee e where 
                        e.employee_id = {emp_id}""".format(emp_id=emp_id))
    emp_name = cur.fetchone()[0]
    cur.execute(""" select s.current_holding,cast(s.credited_on as char),s.salary_amount,coalesce(concat(e.first_name," ",e.last_name),"NA") as accountant  from employee.employee_salary s
                    left join employee.employee e on e.employee_id = s.credited_by
                    where s.employee_id ={emp_id} and s.credited_on ='{date}'
                    order by credited_on desc;""".format(emp_id=emp_id, date=date))
    salary_history = cur.fetchall()
    if salary_history:
        salary_list = [salary for salary in salary_history]
        salary_history = []
        for salary in salary_list:
            salary_dict = {"current_holding": salary[0], "credited_on": salary[1], "salary_credited": str(salary[2]),
                           "credited_by": salary[3]}
            salary_history.append(salary_dict)
        salary_history_details = {"Employee": emp_name, "Salary_History": salary_history}
        return salary_history_details
    else:
        return {"Error": "Salary details not found for the date passed"}
