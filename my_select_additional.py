from sqlalchemy.orm import Session
from sqlalchemy import func, desc, select
from models import Student, Grade, Subject, Teacher, Group, teacher_m2m_subject
from random_util import (
    get_random_subject_name,
    get_random_teacher_name,
    get_random_group_name,
    get_random_student_name,
)


def select_average_grade_teacher_to_student(
    session: Session, teacher_name: str, student_name: str
):
    """Find the average grade given by a specific teacher to a specific student."""
    return (
        session.query(func.avg(Grade.grade).label("average_grade"))
        .join(Subject)
        .join(Subject.teachers)
        .join(Student)
        .filter(Teacher.name == teacher_name, Student.name == student_name)
        .scalar()
    )


def select_grades_last_lesson(session: Session, group_name: str, subject_name: str):
    """Find the grades of students in a specific group for a specific subject on the last lesson."""

    subquery = (
        select(func.max(Grade.date_received))
        .join(Student)
        .join(Group)
        .join(Subject)
        .where(Group.name == group_name, Subject.name == subject_name)
        .scalar_subquery()
    )

    query = (
        select(
            Grade.id.label("grade_id"),
            Student.name.label("student_name"),
            Subject.name.label("subject_name"),
            Grade.grade.label("grade_value"),
            Grade.date_received.label("date_received"),
        )
        .join(Student)
        .join(Group)
        .join(Subject)
        .where(
            Group.name == group_name,
            Subject.name == subject_name,
            Grade.date_received == subquery,
        )
    )

    return session.execute(query).all()


if __name__ == "__main__":
    from connect import session

    teacher_name = get_random_teacher_name(session)
    student_name = get_random_student_name(session)
    group_name = get_random_group_name(session)
    subject_name = get_random_subject_name(session)

    print(f"\nAverage grade given by {teacher_name} to {student_name}:")
    avg_grade = select_average_grade_teacher_to_student(
        session, teacher_name, student_name
    )
    print(f"{avg_grade:.2f}")

    print(
        f"\nGrades of students in group: {group_name} for subject: {subject_name} on the last lesson:"
    )

    grades = select_grades_last_lesson(session, group_name, subject_name)
    for grade in grades:
        grade_id, student_name, subject_name, grade_value, date_received = grade
        print(
            f"Student: {student_name}, Subject: {subject_name}, Grade: {grade_value}, Date: {date_received}"
        )
