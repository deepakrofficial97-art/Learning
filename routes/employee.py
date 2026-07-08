from flask import Blueprint, jsonify
from controllers.employee_controller import (
    get_all_employees as controller_get_all_employees,
    get_employee as controller_get_employee,
    create_employee as controller_create_employee,
    update_employee as controller_update_employee,
    delete_employee as controller_delete_employee,
)

employee_bp = Blueprint("employee", __name__)


@employee_bp.route("/", methods=["GET"])
def get_employees():
    try:
        employees = controller_get_all_employees()
        return jsonify({"data": [employee.to_dict() for employee in employees]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@employee_bp.route("/", methods=["POST"])
def create_employees():
    try:
        employee = controller_create_employee()
        return jsonify({"message": "Employee created", "data": employee.to_dict()}), 201
    except ValueError as e:
        status_code = 409 if "already exists" in str(e).lower() else 400
        return jsonify({"error": str(e)}), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@employee_bp.route("/<int:employee_id>", methods=["GET"])
def get_employee_by_id(employee_id):
    try:
        employee = controller_get_employee(employee_id)
        return jsonify({"data": employee.to_dict()}), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@employee_bp.route("/<int:employee_id>", methods=["PUT"])
def update_employee_by_id(employee_id):
    try:
        employee = controller_update_employee(employee_id)
        return jsonify({"message": "Employee updated", "data": employee.to_dict()}), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@employee_bp.route("/<int:employee_id>", methods=["DELETE"])
def delete_employee_by_id(employee_id):
    try:
        controller_delete_employee(employee_id)
        return jsonify({"message": "Employee deleted"}), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

