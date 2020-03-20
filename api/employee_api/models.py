from django.db import models


# Create your models here.
class Role(models.Model):
    role_name = models.CharField(max_length=50, null=False)

    class Meta:
        db_table = "employee_role"

    def __str__(self):
        return self.role_name


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    manager_id = models.IntegerField(null=False)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True)
    joining_date = models.DateField()

    class Meta:
        db_table = "employee"

    def __str__(self):
        return self.first_name + " " + self.last_name


class Salary(models.Model):
    employee = models.OneToOneField('Employee', on_delete=models.CASCADE, primary_key=True)
    daily_salary = models.FloatField(null=False)
    current_holding = models.FloatField(null=False, default=0)

    class Meta:
        db_table = "employee_salary"

    def __str__(self):
        return "{employee_id} - Salary {salary}".format(employee_id=self.employee_id, salary=self.salary)
