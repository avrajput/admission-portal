from flask import Flask, render_template, redirect, url_for, request, flash, session
from config import Config
from models.user import User
from models.db import db
from models.course import Course, Subject
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename
from models.student import Student
# Removed unused rollno_service import
from datetime import datetime
from routes.admin_routes import admin_bp
from routes.teacher_routes import teacher_bp
from models.student_class import StudentClass
from models.class_model import Class
from models.fee import Fee
from models.payment import Payment
from utils.generate_roll import generate_roll_no
from routes.student_routes import student_bp
from models.attendance import Attendance
from models.branch import Branch 
from models.installment import Installment
from routes.super_admin_routes import super_admin_bp

app = Flask(__name__)
config_name = "config.ProductionConfig" if os.getenv("FLASK_CONFIG") == "production" else "config.DevelopmentConfig"
app.config.from_object(config_name)

UPLOAD_FOLDER = app.config.get("UPLOAD_FOLDER", "static/uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Init DB
db.init_app(app)

# Routes
app.register_blueprint(admin_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(student_bp)
app.register_blueprint(super_admin_bp)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))

    if user and not user.is_active:
        return None

    return user


# Create Tables (run once)
with app.app_context():
    db.create_all()

# ================= AUTH ROUTES ================= #
@app.route("/")
def home():
    logout_user()
    session.clear()
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        logout_user()
        session.clear()

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            if user.role == "student":
                return redirect(url_for("student.student_dashboard"))

            elif user.role == "teacher":
                return redirect(url_for("teacher.teacher_dashboard"))

            elif user.role == "admin":
                return redirect(url_for("admin.admin_dashboard"))

            elif user.role == "super_admin":
                return redirect(url_for("super_admin.dashboard"))
            else:
                flash("Invalid credentials", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("home"))

@app.context_processor
def inject_branch():

    branch = None

    if current_user.is_authenticated and session.get("branch_id"):
        branch = Branch.query.get(session.get("branch_id"))

    return {"current_branch": branch}

@app.context_processor
def inject_global_data():
    from models.branch import Branch
    from flask_login import current_user
    from flask import session

    branches = []
    current_branch = None

    if current_user.is_authenticated and current_user.role == "super_admin":
        branches = Branch.query.all()

    if session.get("branch_id"):
        current_branch = Branch.query.get(session.get("branch_id"))

    return dict(
        branches=branches,
        current_branch=current_branch,
        current_branch_id=session.get("branch_id")
    )

if __name__ == "__main__":
    debug = app.config.get("DEBUG", False)
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=debug, use_reloader=debug)
