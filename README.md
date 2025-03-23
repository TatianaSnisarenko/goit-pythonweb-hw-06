# Student Database Project

## Project Description

This project implements a database for managing students, groups, teachers, subjects, and grades. The database consists of the following tables:

- **Students** table
- **Groups** table
- **Teachers** table
- **Subjects** table
- **Grades** table

## Prerequisites

- Python 3.8+
- Docker

## Usage

### Step 1: Create a Docker Container with PostgreSQL

Run the following command to start a PostgreSQL container:

```sh
docker run --name hw6-db -p 54321:5432 -e POSTGRES_USER=hw6 -e POSTGRES_PASSWORD=hw6pass -d postgres
```

### Step 2: Install Dependencies

Install the required dependencies from `requirements.txt`:

```sh
pip install -r requirements.txt
```

### Step 3: Configure Alembic

Alembic is already set up with the database models. To create and apply the migration, run:

```sh
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Step 4: Populate the Database with Random Data

Run the `seed.py` script to populate the database with random data:

```sh
python seed.py
```

### Step 5: Run Select Queries

You can execute predefined select queries from `my_select.py` and `my_select_additional.py` using the following command:

```sh
python my_select.py
python my_select_additional.py
```

This will run the queries and display the results.

## Running Tests

To run the test suite, use:

```sh
python -m unittest discover -s test -p "test_my_select.py"
python -m unittest discover -s test -p "test_my_select_additional.py"
```
