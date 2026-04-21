from app import app
from models.db import db
from models.course import Subject

with app.app_context():

    subjects_list = [
        "Python",
        "JavaScript",
        "HTML",
        "CSS",
        "React",
        "SQL",
        "Data Structures",
        "Machine Learning"
    ]

    for name in subjects_list:
        existing = Subject.query.filter_by(name=name).first()

        if not existing:
            subject = Subject(name=name)
            db.session.add(subject)
        else:
            print(f"Already exists: {name}")

    db.session.commit()

    print("Subjects inserted successfully")