import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Base, Student, Grade, Subject, Teacher, Group, teacher_m2m_subject
from my_select import (
    select_1,
    select_2,
    select_3,
    select_4,
    select_5,
    select_6,
    select_7,
    select_8,
    select_9,
    select_10,
    get_random_subject_name,
    get_random_teacher_name,
    get_random_group_name,
    get_random_student_name,
)


class TestMySelect(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create an in-memory SQLite database
        cls.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

        # Populate the database with test data
        cls.populate_database()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        cls.engine.dispose()

    @classmethod
    def populate_database(cls):
        # Add test data to the database
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

        grade1 = Grade(student_id=student1.id, subject_id=subject1.id, grade=85)
        grade2 = Grade(student_id=student2.id, subject_id=subject1.id, grade=90)
        grade3 = Grade(student_id=student3.id, subject_id=subject2.id, grade=95)
        cls.session.add_all([grade1, grade2, grade3])
        cls.session.commit()

    def test_select_1(self):
        result = select_1(self.session)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].name, "Student 3")
        self.assertAlmostEqual(result[0].average_grade, 95.0, places=2)

    def test_select_2(self):
        result = select_2(self.session, "Math")
        self.assertEqual(result.name, "Student 2")
        self.assertAlmostEqual(result.average_grade, 90.0, places=2)

    def test_select_3(self):
        result = select_3(self.session, "Math")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Group 1")
        self.assertAlmostEqual(result[0].average_grade, 87.5, places=2)

    def test_select_4(self):
        result = select_4(self.session)
        self.assertAlmostEqual(result, 90.0, places=2)

    def test_select_5(self):
        result = select_5(self.session, "Teacher 1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Math")

    def test_select_6(self):
        result = select_6(self.session, "Group 1")
        self.assertEqual(len(result), 2)
        self.assertIn("Student 1", [student.name for student in result])
        self.assertIn("Student 2", [student.name for student in result])

    def test_select_7(self):
        result = select_7(self.session, "Group 1", "Math")
        self.assertEqual(len(result), 2)
        self.assertIn(("Student 1", 85), result)
        self.assertIn(("Student 2", 90), result)

    def test_select_8(self):
        result = select_8(self.session, "Teacher 1")
        self.assertAlmostEqual(result, 87.5, places=2)

    def test_select_9(self):
        result = select_9(self.session, "Student 1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Math")

    def test_select_10(self):
        result = select_10(self.session, "Student 1", "Teacher 1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Math")

    def test_get_random_subject_name(self):
        result = get_random_subject_name(self.session)
        self.assertIn(result, ["Math", "Science"])

    def test_get_random_teacher_name(self):
        result = get_random_teacher_name(self.session)
        self.assertIn(result, ["Teacher 1", "Teacher 2"])

    def test_get_random_group_name(self):
        result = get_random_group_name(self.session)
        self.assertIn(result, ["Group 1", "Group 2"])

    def test_get_random_student_name(self):
        result = get_random_student_name(self.session)
        self.assertIn(result, ["Student 1", "Student 2", "Student 3"])


if __name__ == "__main__":
    unittest.main()
