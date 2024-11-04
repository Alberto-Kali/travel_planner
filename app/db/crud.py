from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from app.models.user import User
from app.models.trip import Trip, TripDay, PlaceVisit, Place

class CRUDUser:
    @staticmethod
    def create(db: Session, username: str, email: str, hashed_password: str) -> User:
        db_user = User(username=username, email=email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_by_username(db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

class CRUDPlace:
    @staticmethod
    def create(db: Session, obj_in: Dict) -> Place:
        db_place = Place(**obj_in)
        db.add(db_place)
        db.commit()
        db.refresh(db_place)
        return db_place

    @staticmethod
    def get_all(db: Session) -> List[Place]:
        return db.query(Place).all()

    @staticmethod
    def get_by_id(db: Session, place_id: int) -> Optional[Place]:
        return db.query(Place).filter(Place.id == place_id).first()

class CRUDTrip:
    @staticmethod
    def create(db: Session, user_id: int, title: str, description: str,
               start_date: str, end_date: str) -> Trip:
        db_trip = Trip(
            user_id=user_id,
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date
        )
        db.add(db_trip)
        db.commit()
        db.refresh(db_trip)
        return db_trip

    @staticmethod
    def get_user_trips(db: Session, user_id: int) -> List[Trip]:
        return db.query(Trip).filter(Trip.user_id == user_id).all()

    @staticmethod
    def add_day(db: Session, trip_id: int, day_number: int,
                total_distance_km: float, total_time_hours: float,
                transport: str) -> TripDay:
        db_day = TripDay(
            trip_id=trip_id,
            day_number=day_number,
            total_distance_km=total_distance_km,
            total_time_hours=total_time_hours,
            transport=transport
        )
        db.add(db_day)
        db.commit()
        db.refresh(db_day)
        return db_day
