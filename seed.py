from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Student, Group, Teacher, Subject, Grade
import random
from datetime import datetime, timedelta
from logger_provider import console_logger

from connect import session

logger = console_logger("Seed")

if __name__ == "__main__":

    fake = Faker()

    groups = [Group(name=fake.unique.word()) for _ in range(3)]
    session.add_all(groups)
    session.commit()

    teachers = [Teacher(name=fake.name()) for _ in range(5)]
    session.add_all(teachers)
    session.commit()

    subjects = [Subject(name=fake.word()) for _ in range(8)]
    session.add_all(subjects)
    session.commit()

    for subject in subjects:
        subject.teachers = random.sample(teachers, random.randint(1, len(teachers)))
    session.commit()

    students = []
    for _ in range(50):
        student = Student(name=fake.name(), group=random.choice(groups))
        students.append(student)
    session.add_all(students)
    session.commit()

    for student in students:
        for subject in subjects:
            for _ in range(random.randint(10, 20)):
                grade = Grade(
                    student_id=student.id,
                    subject_id=subject.id,
                    grade=random.randint(60, 100),
                    date_received=fake.date_time_between(
                        start_date="-1y", end_date="now"
                    ),
                )
                session.add(grade)

    session.commit()
    session.close()

    logger.info("Db is filled with fake data")
