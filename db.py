import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine(os.getenv("DATABASE_URL"))

DBSession = sessionmaker(bind=engine)
session = scoped_session(DBSession)
