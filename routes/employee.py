from flask import Blueprint, jsonify
from controllers.employee_controller import (
    get_all_employees,
    get_employee,
    create_employee,
    update_employee,
    delete_employee
)
employee_bp = Blueprint("employee", __name__)


@employee_bp.route("/", methods=["GET"])
def get_employees():
    return jsonify({"message": "Employee list"}), 200


@employee_bp.route("/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    return jsonify({"message": f"Employee {employee_id}"}), 200

