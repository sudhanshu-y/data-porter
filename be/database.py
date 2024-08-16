# Module to handle the database connection using SQLAlchemy

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from be.config import DATABASE_URL

# Create the SQLAlchemy engine
# engine as a connection to your database
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
# Session objects, which manage interactions with the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create MetaData instance
# MetaData is a container - stores information about the schema of the database
# Ex: Table names, Column definitions (name, type, constraints), PK, FK, Indexes
# It does not hold any data or state 
metadata = MetaData(bind=engine)
