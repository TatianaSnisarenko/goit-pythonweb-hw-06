from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Student, Grade, Subject, Teacher, Group, teacher_m2m_subject
from connect import session
from collections import defaultdict
from random_util import (
    get_random_subject_name,
    get_random_teacher_name,
    get_random_group_name,
    get_random_student_name,
)


def select_1(session: Session):
    """Find the top 5 students with the highest average grade across all subjects."""
    return (
        session.query(
            Student.name.label("name"), func.avg(Grade.grade).label("average_grade")
        )
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )


def select_2(session: Session, subject_name: str):
    """Find the student with the highest average grade in a specific subject."""
    return (
        session.query(
            Student.name.label("name"),
            func.avg(Grade.grade).label("average_grade"),
        )
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )


def select_3(session: Session, subject_name: str):
    """Find the average grade in groups for a specific subject."""
    return (
        session.query(
            Group.name.label("name"), func.avg(Grade.grade).label("average_grade")
        )
        .select_from(Group)
        .join(Student, Group.id == Student.group_id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Group.id)
        .all()
    )


def select_4(session: Session):
    """Find the average grade across all grades."""
    return session.query(func.avg(Grade.grade)).scalar()


def select_5(session: Session, teacher_name: str):
    """Find the courses taught by a specific teacher."""
    return (
        session.query(Subject.name)
        .join(teacher_m2m_subject, Subject.id == teacher_m2m_subject.c.subject_id)
        .join(Teacher, teacher_m2m_subject.c.teacher_id == Teacher.id)
        .filter(Teacher.name == teacher_name)
        .all()
    )


def select_6(session: Session, group_name: str):
    """Find the list of students in a specific group."""
    return (
        session.query(Student.name).join(Group).filter(Group.name == group_name).all()
    )


def select_7(session: Session, group_name: str, subject_name: str):
    """Find the grades of students in a specific group for a specific subject."""
    return (
        session.query(Student.name, Grade.grade)
        .join(Group)
        .join(Grade)
        .join(Subject)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )


def select_8(session: Session, teacher_name: str):
    """Find the average grade given by a specific teacher across their subjects."""
    return (
        session.query(func.avg(Grade.grade).label("average_grade"))
        .join(Subject)
        .join(Subject.teachers)
        .filter(Teacher.name == teacher_name)
        .scalar()
    )


def select_9(session: Session, student_name: str):
    """Find the list of courses attended by a specific student."""
    return (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .filter(Student.name == student_name)
        .distinct()
        .all()
    )


def select_10(session: Session, student_name: str, teacher_name: str):
    """Find the list of courses taught by a specific teacher to a specific student."""
    return (
        session.query(Subject.name)
        .join(Grade)
        .join(Subject.teachers)
        .join(Student)
        .filter(Student.name == student_name, Teacher.name == teacher_name)
        .distinct()
        .all()
    )


if __name__ == "__main__":
    print("Top 5 students with the highest average grade across all subjects:")
    top_students = select_1(session)
    for student in top_students:
        print(f"{student.name} - {student.average_grade:.2f}")

    random_subject = get_random_subject_name(session)
    print(
        f"\nStudent with the highest average grade in a specific subject (subject_name={random_subject}):"
    )
    student_for_subject = select_2(session, random_subject)
    print(f"{student_for_subject.name} - {student_for_subject.average_grade:.2f}")

    print(
        f"\nAverage grade in groups for a specific subject (subject={random_subject}):"
    )
    groups = select_3(session, random_subject)
    for group in groups:
        print(f"{group.name} - {group.average_grade:.2f}")

    print("\nAverage grade across all grades:")
    avg_grade = select_4(session)
    print(f"{avg_grade:.2f}")

    random_teacher = get_random_teacher_name(session)

    print(f"\nCourses taught by a specific teacher (teacher_id={random_teacher}):")
    courses = select_5(session, random_teacher)
    print(", ".join(course.name for course in courses))

    random_group = get_random_group_name(session)

    print(f"\nList of students in a specific group (group_name={random_group}):")
    students = select_6(session, random_group)
    print(", ".join(student.name for student in students))

    print(
        f"\nGrades of students in a specific group (group={random_group}) for a specific subject (subject={random_subject}):"
    )
    grades = select_7(session, random_group, random_subject)
    student_grades = defaultdict(list)
    for student, grade in grades:
        student_grades[student].append(grade)

    for student, grades in student_grades.items():
        grades_str = ", ".join(str(grade) for grade in grades)
        print(f"{student} - ({grades_str})")

    print(
        f"\nAverage grade given by a specific teacher (teacher_name={random_teacher}) across their subjects:"
    )
    print(f"{select_8(session, random_teacher):.2f}")

    random_student = get_random_student_name(session)

    print(
        f"\nList of courses attended by a specific student (student_name={random_student}):"
    )
    courses = select_9(session, random_student)
    print(", ".join(course.name for course in courses))

    random_student = get_random_student_name(session)
    random_teacher = get_random_teacher_name(session)

    print(
        f"\nList of courses taught by a specific teacher (teacher_name={random_teacher}) to a specific student (student_name={random_student}):"
    )
    courses = select_10(session, random_student, random_teacher)
    print(", ".join(course.name for course in courses))
