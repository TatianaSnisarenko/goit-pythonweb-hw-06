from sqlalchemy.orm import Session
from models import Student, Grade, Subject, Teacher, Group, teacher_m2m_subject
from connect import session
import random


def get_random_subject_name(session: Session):
    """Get a random subject name from the database."""
    subjects = session.query(Subject.name).join(Grade).distinct().all()
    return random.choice(subjects).name


def get_random_teacher_name(session: Session):
    """Get a random teacher name from the database."""
    teachers = (
        session.query(Teacher.name)
        .join(teacher_m2m_subject, Teacher.id == teacher_m2m_subject.c.teacher_id)
        .join(Subject, teacher_m2m_subject.c.subject_id == Subject.id)
        .join(Grade, Grade.subject_id == Subject.id)
        .distinct()
        .all()
    )
    return random.choice(teachers).name


def get_random_group_name(session: Session):
    """Get a random group name from the database that has students."""
    groups = session.query(Group.name).join(Student).distinct().all()
    return random.choice(groups).name


def get_random_student_name(session: Session):
    """Get a random student name from the database."""
    students = session.query(Student.name).distinct().all()
    return random.choice(students).name
