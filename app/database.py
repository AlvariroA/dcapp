from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
SQLALCHEMY_DATABASE_URL = "postgresql://ueniqeyafvvivh:3e386f00a4e558cfbaabb77da612878e70392332947b90eea3d3328b2b528c03@ec2-54-147-33-38.compute-1.amazonaws.com:5432/d23cemb0go55pp"
 

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()