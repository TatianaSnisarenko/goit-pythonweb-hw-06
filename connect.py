from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

url_to_db = "postgresql+pg8000://hw6:hw6pass@localhost:54321/postgres"

engine = create_engine(url_to_db)
Session = sessionmaker(bind=engine)
session = Session()
