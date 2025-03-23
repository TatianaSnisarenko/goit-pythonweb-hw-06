import argparse
from sqlalchemy.orm import sessionmaker
from connect import engine
from models import Base, Student, Group, Teacher, Subject, Grade
from sqlalchemy.exc import NoResultFound

Session = sessionmaker(bind=engine)
session = Session()


def create_teacher(name):
    teacher = Teacher(name=name)
    session.add(teacher)
    session.commit()
    print(f"Teacher '{name}' created with ID {teacher.id}")


def list_teachers():
    teachers = session.query(Teacher).all()
    for teacher in teachers:
        print(f"ID: {teacher.id}, Name: {teacher.name}")


def update_teacher(teacher_id, name):
    try:
        teacher = session.query(Teacher).filter(Teacher.id == teacher_id).one()
        teacher.name = name
        session.commit()
        print(f"Teacher with ID {teacher_id} updated to '{name}'")
    except NoResultFound:
        print(f"No teacher found with ID {teacher_id}")


def remove_teacher(teacher_id):
    try:
        teacher = session.query(Teacher).filter(Teacher.id == teacher_id).one()
        session.delete(teacher)
        session.commit()
        print(f"Teacher with ID {teacher_id} removed")
    except NoResultFound:
        print(f"No teacher found with ID {teacher_id}")


def create_group(name):
    group = Group(name=name)
    session.add(group)
    session.commit()
    print(f"Group '{name}' created with ID {group.id}")


def list_groups():
    groups = session.query(Group).all()
    for group in groups:
        print(f"ID: {group.id}, Name: {group.name}")


def update_group(group_id, name):
    try:
        group = session.query(Group).filter(Group.id == group_id).one()
        group.name = name
        session.commit()
        print(f"Group with ID {group_id} updated to '{name}'")
    except NoResultFound:
        print(f"No group found with ID {group_id}")


def remove_group(group_id):
    try:
        group = session.query(Group).filter(Group.id == group_id).one()
        session.delete(group)
        session.commit()
        print(f"Group with ID {group_id} removed")
    except NoResultFound:
        print(f"No group found with ID {group_id}")


def create_student(name, group_id):
    try:
        group = session.query(Group).filter(Group.id == group_id).one()
        student = Student(name=name, group_id=group.id)
        session.add(student)
        session.commit()
        print(f"Student '{name}' created with ID {student.id} in group '{group.name}'")
    except NoResultFound:
        print(f"No group found with ID {group_id}")


def list_students():
    students = session.query(Student).all()
    for student in students:
        print(f"ID: {student.id}, Name: {student.name}, Group ID: {student.group_id}")


def update_student(student_id, name, group_id):
    try:
        student = session.query(Student).filter(Student.id == student_id).one()
        student.name = name
        student.group_id = group_id
        session.commit()
        print(
            f"Student with ID {student_id} updated to '{name}' in group ID {group_id}"
        )
    except NoResultFound:
        print(f"No student found with ID {student_id}")


def remove_student(student_id):
    try:
        student = session.query(Student).filter(Student.id == student_id).one()
        session.delete(student)
        session.commit()
        print(f"Student with ID {student_id} removed")
    except NoResultFound:
        print(f"No student found with ID {student_id}")


def create_subject(name):
    subject = Subject(name=name)
    session.add(subject)
    session.commit()
    print(f"Subject '{name}' created with ID {subject.id}")


def list_subjects():
    subjects = session.query(Subject).all()
    for subject in subjects:
        print(f"ID: {subject.id}, Name: {subject.name}")


def update_subject(subject_id, name):
    try:
        subject = session.query(Subject).filter(Subject.id == subject_id).one()
        subject.name = name
        session.commit()
        print(f"Subject with ID {subject_id} updated to '{name}'")
    except NoResultFound:
        print(f"No subject found with ID {subject_id}")


def remove_subject(subject_id):
    try:
        subject = session.query(Subject).filter(Subject.id == subject_id).one()
        session.delete(subject)
        session.commit()
        print(f"Subject with ID {subject_id} removed")
    except NoResultFound:
        print(f"No subject found with ID {subject_id}")


def create_grade(student_id, subject_id, grade_value, date_received):
    try:
        student = session.query(Student).filter(Student.id == student_id).one()
        subject = session.query(Subject).filter(Subject.id == subject_id).one()
        grade = Grade(
            student_id=student.id,
            subject_id=subject.id,
            grade=grade_value,
            date_received=date_received,
        )
        session.add(grade)
        session.commit()
        print(
            f"Grade '{grade_value}' created for student '{student.name}' in subject '{subject.name}'"
        )
    except NoResultFound:
        print(f"No student or subject found with the provided IDs")


def list_grades():
    grades = session.query(Grade).all()
    for grade in grades:
        print(
            f"ID: {grade.id}, Student ID: {grade.student_id}, Subject ID: {grade.subject_id}, Grade: {grade.grade}, Date Received: {grade.date_received}"
        )


def update_grade(grade_id, grade_value, date_received):
    try:
        grade = session.query(Grade).filter(Grade.id == grade_id).one()
        grade.grade = grade_value
        grade.date_received = date_received
        session.commit()
        print(
            f"Grade with ID {grade_id} updated to '{grade_value}' on '{date_received}'"
        )
    except NoResultFound:
        print(f"No grade found with ID {grade_id}")


def remove_grade(grade_id):
    try:
        grade = session.query(Grade).filter(Grade.id == grade_id).one()
        session.delete(grade)
        session.commit()
        print(f"Grade with ID {grade_id} removed")
    except NoResultFound:
        print(f"No grade found with ID {grade_id}")


def main():
    parser = argparse.ArgumentParser(description="CRUD operations for the database")
    parser.add_argument(
        "-a",
        "--action",
        required=True,
        choices=["create", "list", "update", "remove"],
        help="CRUD action",
    )
    parser.add_argument(
        "-m",
        "--model",
        required=True,
        choices=["Teacher", "Group", "Student", "Subject", "Grade"],
        help="Model to perform action on",
    )
    parser.add_argument("--id", type=int, help="ID of the record to update or remove")
    parser.add_argument(
        "--name", type=str, help="Name of the record to create or update"
    )
    parser.add_argument(
        "--group_id", type=int, help="Group ID for creating or updating a student"
    )
    parser.add_argument(
        "--student_id", type=int, help="Student ID for creating or updating a grade"
    )
    parser.add_argument(
        "--subject_id", type=int, help="Subject ID for creating or updating a grade"
    )
    parser.add_argument(
        "--grade_value", type=int, help="Grade value for creating or updating a grade"
    )
    parser.add_argument(
        "--date_received",
        type=str,
        help="Date received for creating or updating a grade",
    )

    args = parser.parse_args()

    if args.model == "Teacher":
        if args.action == "create":
            if args.name:
                create_teacher(args.name)
            else:
                print("Name is required to create a teacher")
        elif args.action == "list":
            list_teachers()
        elif args.action == "update":
            if args.id and args.name:
                update_teacher(args.id, args.name)
            else:
                print("ID and name are required to update a teacher")
        elif args.action == "remove":
            if args.id:
                remove_teacher(args.id)
            else:
                print("ID is required to remove a teacher")

    elif args.model == "Group":
        if args.action == "create":
            if args.name:
                create_group(args.name)
            else:
                print("Name is required to create a group")
        elif args.action == "list":
            list_groups()
        elif args.action == "update":
            if args.id and args.name:
                update_group(args.id, args.name)
            else:
                print("ID and name are required to update a group")
        elif args.action == "remove":
            if args.id:
                remove_group(args.id)
            else:
                print("ID is required to remove a group")

    elif args.model == "Student":
        if args.action == "create":
            if args.name and args.group_id:
                create_student(args.name, args.group_id)
            else:
                print("Name and group ID are required to create a student")
        elif args.action == "list":
            list_students()
        elif args.action == "update":
            if args.id and args.name and args.group_id:
                update_student(args.id, args.name, args.group_id)
            else:
                print("ID, name, and group ID are required to update a student")
        elif args.action == "remove":
            if args.id:
                remove_student(args.id)
            else:
                print("ID is required to remove a student")

    elif args.model == "Subject":
        if args.action == "create":
            if args.name:
                create_subject(args.name)
            else:
                print("Name is required to create a subject")
        elif args.action == "list":
            list_subjects()
        elif args.action == "update":
            if args.id and args.name:
                update_subject(args.id, args.name)
            else:
                print("ID and name are required to update a subject")
        elif args.action == "remove":
            if args.id:
                remove_subject(args.id)
            else:
                print("ID is required to remove a subject")

    elif args.model == "Grade":
        if args.action == "create":
            if (
                args.student_id
                and args.subject_id
                and args.grade_value
                and args.date_received
            ):
                create_grade(
                    args.student_id,
                    args.subject_id,
                    args.grade_value,
                    args.date_received,
                )
            else:
                print(
                    "Student ID, subject ID, grade value, and date received are required to create a grade"
                )
        elif args.action == "list":
            list_grades()
        elif args.action == "update":
            if args.id and args.grade_value and args.date_received:
                update_grade(args.id, args.grade_value, args.date_received)
            else:
                print(
                    "ID, grade value, and date received are required to update a grade"
                )
        elif args.action == "remove":
            if args.id:
                remove_grade(args.id)
            else:
                print("ID is required to remove a grade")


if __name__ == "__main__":
    main()
