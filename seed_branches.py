from app import app
from models.db import db
from models.branch import Branch

with app.app_context():

    branches = [
        {"name": "Saket", "location": "Delhi"},
        {"name": "Devli", "location": "Delhi"},
        {"name": "South Extension", "location": "Delhi"}
    ]

    for b in branches:
        existing = Branch.query.filter_by(name=b["name"]).first()

        if not existing:
            branch = Branch(
                name=b["name"],
                location=b["location"]
            )
            db.session.add(branch)

    db.session.commit()

    print("Branches inserted successfully")