from flask import request, jsonify
from extensions import db
from models.employee_model import Employee


def get_all_employees():
    employees = Employee.query.filter_by(is_active=True).all()
    return jsonify({"data": [e.to_dict() for e in employees]}), 200


def get_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify({"data": employee.to_dict()}), 200


def create_employee():
    data = request.get_json()

    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "name and email are required"}), 400

    if Employee.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 409

    employee = Employee(
        name       = data["name"],
        email      = data["email"],
        department = data.get("department"),
        salary     = data.get("salary"),
    )
    db.session.add(employee)
    db.session.commit()
    return jsonify({"message": "Employee created", "data": employee.to_dict()}), 201


def update_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    data = request.get_json()
    employee.name       = data.get("name", employee.name)
    employee.email      = data.get("email", employee.email)
    employee.department = data.get("department", employee.department)
    employee.salary     = data.get("salary", employee.salary)

    db.session.commit()
    return jsonify({"message": "Employee updated", "data": employee.to_dict()}), 200


def delete_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    employee.is_active = False   # soft delete
    db.session.commit()
    return jsonify({"message": "Employee deleted"}), 200