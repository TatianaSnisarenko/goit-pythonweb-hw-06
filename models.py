from datetime import datetime
from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    String,
    DateTime,
    Table,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


teacher_m2m_subject = Table(
    "teacher_m2m_subject",
    Base.metadata,
    Column("teacher_id", ForeignKey("teachers.id"), primary_key=True),
    Column("subject_id", ForeignKey("subjects.id"), primary_key=True),
    PrimaryKeyConstraint("teacher_id", "subject_id"),
)


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))

    group = relationship("Group", back_populates="students", cascade="all")
    grades = relationship(
        "Grade", back_populates="student", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}', group_id={self.group_id})>"


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    students = relationship(
        "Student", back_populates="group", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Group(id={self.id}, name='{self.name}')>"


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    subjects = relationship(
        "Subject", secondary=teacher_m2m_subject, back_populates="teachers"
    )

    def __repr__(self):
        return f"<Teacher(id={self.id}, name='{self.name}')>"


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    teachers = relationship(
        "Teacher", secondary=teacher_m2m_subject, back_populates="subjects"
    )
    grades = relationship(
        "Grade", back_populates="subject", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Subject(id={self.id}, name='{self.name}')>"


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    date_received: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")

    def __repr__(self):
        return f"<Grade(id={self.id}, student_id={self.student_id}, subject_id={self.subject_id}, grade={self.grade}, date_received={self.date_received})>"
