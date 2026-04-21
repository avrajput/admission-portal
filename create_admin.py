from app import app
from models.db import db
from models.user import User
from models.branch import Branch
from werkzeug.security import generate_password_hash

with app.app_context():

    # GET BRANCH (SAKET)
    saket_branch = Branch.query.filter_by(name="Saket").first()

    if not saket_branch:
        print("Saket branch not found. Run branch seeder first.")
        exit()

    # SUPER ADMIN (NO BRANCH)
    super_admin = User.query.filter_by(email="super@techno.com").first()

    if not super_admin:
        super_admin = User(
            name="Super Admin",
            email="super@techno.com",
            password=generate_password_hash("123456"),
            role="super_admin",
            branch_id=None   # IMPORTANT
        )
        db.session.add(super_admin)

    # ADMIN (SAKET BRANCH)
    admin = User.query.filter_by(email="admin@techno.com").first()

    if not admin:
        admin = User(
            name="Admin Saket",
            email="admin@techno.com",
            password=generate_password_hash("123456"),
            role="admin",
            branch_id=saket_branch.id   # FK
        )
        db.session.add(admin)

    db.session.commit()

    print("Admin & Super Admin created successfully")