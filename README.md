# Student Database Project

## Project Description

This project implements a database system for managing students, groups, teachers, subjects, and grades. The database consists of the following tables:

- **Students**
- **Groups**
- **Teachers**
- **Subjects**
- **Grades**

## Prerequisites

- Python 3.8+
- Docker

## Setup and Usage

### Step 1: Start a PostgreSQL Container

Run the following command to start a PostgreSQL container:

```sh
docker run --name hw6-db -p 54321:5432 -e POSTGRES_USER=hw6 -e POSTGRES_PASSWORD=hw6pass -d postgres
```

### Step 2: Install Dependencies

Install the required dependencies from `requirements.txt`:

```sh
pip install -r requirements.txt
```

### Step 3: Configure and Apply Migrations

Alembic is set up to manage database migrations. To create and apply the initial migration, run:

```sh
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Step 4: Populate the Database with Sample Data

Use the `seed.py` script to populate the database with random data:

```sh
python seed.py
```

### Step 5: Run Queries

Execute predefined select queries using:

```sh
python my_select.py
python my_select_additional.py
```

## Running Tests

To run the test suite, execute:

```sh
python -m unittest discover -s test -p "test_*.py"
```

## Performing CRUD Operations via CLI

The `main.py` script allows CRUD operations on the database using terminal commands. It utilizes `argparse` for command-line arguments.

### General Usage

```sh
python main.py -a <action> -m <model> [additional arguments]
```

- `-a` or `--action`: CRUD action (`create`, `list`, `update`, `remove`)
- `-m` or `--model`: Target model (`Teacher`, `Group`, `Student`, `Subject`, `Grade`)

### Commands

#### Teachers

**Create a Teacher:**

```sh
python main.py -a create -m Teacher --name "Boris Johnson"
```

**List All Teachers:**

```sh
python main.py -a list -m Teacher
```

**Update a Teacher:**

```sh
python main.py -a update -m Teacher --id <teacher_id> --name "Andrew Bezos"
```

**Remove a Teacher:**

```sh
python main.py -a remove -m Teacher --id <teacher_id>
```

#### Groups

**Create a Group:**

```sh
python main.py -a create -m Group --name "AD-101"
```

**List All Groups:**

```sh
python main.py -a list -m Group
```

**Update a Group:**

```sh
python main.py -a update -m Group --id <group_id> --name "BD-202"
```

**Remove a Group:**

```sh
python main.py -a remove -m Group --id <group_id>
```

#### Students

**Create a Student:**

```sh
python main.py -a create -m Student --name "John Doe" --group_id <group_id>
```

**List All Students:**

```sh
python main.py -a list -m Student
```

**Update a Student:**

```sh
python main.py -a update -m Student --id <student_id> --name "Jane Doe" --group_id <group_id>
```

**Remove a Student:**

```sh
python main.py -a remove -m Student --id <student_id>
```

#### Subjects

**Create a Subject:**

```sh
python main.py -a create -m Subject --name "Mathematics"
```

**List All Subjects:**

```sh
python main.py -a list -m Subject
```

**Update a Subject:**

```sh
python main.py -a update -m Subject --id <subject_id> --name "Physics"
```

**Remove a Subject:**

```sh
python main.py -a remove -m Subject --id <subject_id>
```

#### Grades

**Create a Grade:**

```sh
python main.py -a create -m Grade --student_id <student_id> --subject_id <subject_id> --grade_value 95 --date_received "2025-03-16 17:41:59"
```

**List All Grades:**

```sh
python main.py -a list -m Grade
```

**Update a Grade:**

```sh
python main.py -a update -m Grade --id <grade_id> --grade_value 98 --date_received "2025-03-17 10:00:00"
```

**Remove a Grade:**

```sh
python main.py -a remove -m Grade --id <grade_id>
```

## Notes

- Replace `<teacher_id>`, `<group_id>`, `<student_id>`, `<subject_id>`, and `<grade_id>` with actual IDs from your database.
- The `date_received` for grades should follow the format `'YYYY-MM-DD HH:MM:SS'`.
