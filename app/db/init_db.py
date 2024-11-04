from sqlalchemy.orm import Session
from app.db.base import Base, engine
from app.models import user, trip

def init_db():
    Base.metadata.create_all(bind=engine)