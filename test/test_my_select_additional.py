import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Base, Student, Grade, Subject, Teacher, Group, teacher_m2m_subject
from my_select_additional import (
    select_average_grade_teacher_to_student,
    select_grades_last_lesson,
)
from random_util import (
    get_random_subject_name,
    get_random_teacher_name,
    get_random_group_name,
    get_random_student_name,
)


class TestMySelectAdditional(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()
        cls.populate_database()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        cls.engine.dispose()

    @classmethod
    def populate_database(cls):
        group1 = Group(name="Group 1")
        group2 = Group(name="Group 2")
        cls.session.add_all([group1, group2])
        cls.session.commit()

        student1 = Student(name="Student 1", group_id=group1.id)
        student2 = Student(name="Student 2", group_id=group1.id)
        student3 = Student(name="Student 3", group_id=group2.id)
        cls.session.add_all([student1, student2, student3])
        cls.session.commit()

        subject1 = Subject(name="Math")
        subject2 = Subject(name="Science")
        cls.session.add_all([subject1, subject2])
        cls.session.commit()

        teacher1 = Teacher(name="Teacher 1")
        teacher2 = Teacher(name="Teacher 2")
        cls.session.add_all([teacher1, teacher2])
        cls.session.commit()

        teacher1.subjects.append(subject1)
        teacher2.subjects.append(subject2)
        cls.session.commit()

        grade1 = Grade(
            student_id=student1.id,
            subject_id=subject1.id,
            grade=85,
            date_received=datetime.strptime("2025-03-16 17:41:59", "%Y-%m-%d %H:%M:%S"),
        )
        grade2 = Grade(
            student_id=student2.id,
            subject_id=subject1.id,
            grade=90,
            date_received=datetime.strptime("2025-03-16 17:41:59", "%Y-%m-%d %H:%M:%S"),
        )
        grade3 = Grade(
            student_id=student3.id,
            subject_id=subject2.id,
            grade=95,
            date_received=datetime.strptime("2025-03-16 17:41:59", "%Y-%m-%d %H:%M:%S"),
        )
        cls.session.add_all([grade1, grade2, grade3])
        cls.session.commit()

    def test_select_average_grade_teacher_to_student(self):
        teacher_name = "Teacher 1"
        student_name = "Student 1"
        result = select_average_grade_teacher_to_student(
            self.session, teacher_name, student_name
        )
        self.assertAlmostEqual(result, 85.0, places=2)

    def test_select_grades_last_lesson(self):
        group_name = "Group 1"
        subject_name = "Math"
        result = select_grades_last_lesson(self.session, group_name, subject_name)
        expected = [
            (1, "Student 1", "Math", 85, "2025-03-16 17:41:59"),
            (2, "Student 2", "Math", 90, "2025-03-16 17:41:59"),
        ]
        self.assertEqual(len(result), len(expected))
        for res, exp in zip(result, expected):
            self.assertEqual(res.grade_id, exp[0])
            self.assertEqual(res.student_name, exp[1])
            self.assertEqual(res.subject_name, exp[2])
            self.assertEqual(res.grade_value, exp[3])
            self.assertEqual(str(res.date_received), exp[4])


if __name__ == "__main__":
    unittest.main()
