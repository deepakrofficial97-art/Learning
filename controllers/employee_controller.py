from flask import request
from models.employee_model import Employee


def get_all_employees():
    return Employee.get_all_active()


def get_employee(employee_id):
    employee = Employee.get_by_id(employee_id)
    if not employee:
        raise LookupError("Employee not found")
    return employee


def create_employee():
    data = request.get_json(silent=True) or {}

    if not data.get("name") or not data.get("email"):
        raise ValueError("name and email are required")

    if Employee.get_by_email(data["email"]):
        raise ValueError("Email already exists")

    return Employee.create_employee(
        name=data["name"],
        email=data["email"],
        department=data.get("department"),
        salary=data.get("salary"),
    )


def update_employee(employee_id):
    employee = Employee.get_by_id(employee_id)
    if not employee:
        raise LookupError("Employee not found")

    data = request.get_json(silent=True) or {}
    return Employee.update_employee(employee, data)


def delete_employee(employee_id):
    employee = Employee.get_by_id(employee_id)
    if not employee:
        raise LookupError("Employee not found")

    return Employee.delete_employee(employee)