from extensions import db
from datetime import datetime


class Employee(db.Model):
    __tablename__ = "employees"

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(150), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=True)
    salary     = db.Column(db.Float, nullable=True)
    is_active  = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def get_all_active(cls):
        return cls.query.filter_by(is_active=True).all()

    @classmethod
    def get_by_id(cls, employee_id):
        return cls.query.get(employee_id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def create_employee(cls, name, email, department=None, salary=None):
        employee = cls(
            name=name,
            email=email,
            department=department,
            salary=salary,
        )
        db.session.add(employee)
        db.session.commit()
        return employee

    @classmethod
    def update_employee(cls, employee, data):
        employee.name = data.get("name", employee.name)
        employee.email = data.get("email", employee.email)
        employee.department = data.get("department", employee.department)
        employee.salary = data.get("salary", employee.salary)
        db.session.commit()
        return employee

    @classmethod
    def delete_employee(cls, employee):
        employee.is_active = False
        db.session.commit()
        return employee

    def to_dict(self):
        return {
            "id":         self.id,
            "name":       self.name,
            "email":      self.email,
            "department": self.department,
            "salary":     self.salary,
            "is_active":  self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

        