from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.user import User
from app.models.trip import Trip, TripDay, PlaceVisit, Place

class DBService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, username: str, email: str, hashed_password: str) -> User:
        db_user = User(username=username, email=email, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def create_trip(self, user_id: int, title: str, description: str, start_date: str, end_date: str) -> Trip:
        db_trip = Trip(user_id=user_id, title=title, description=description, start_date=start_date, end_date=end_date)
        self.db.add(db_trip)
        self.db.commit()
        self.db.refresh(db_trip)
        return db_trip

    def add_trip_day(self, trip_id: int, day_number: int, total_distance_km: float, total_time_hours: float, transport: str) -> TripDay:
        db_trip_day = TripDay(
            trip_id=trip_id, 
            day_number=day_number, 
            total_distance_km=total_distance_km, 
            total_time_hours=total_time_hours, 
            transport=transport
        )
        self.db.add(db_trip_day)
        self.db.commit()
        self.db.refresh(db_trip_day)
        return db_trip_day

    def add_place(self, name: str, description: str, photo_link: str) -> Place:
        db_place = Place(name=name, description=description, photo_link=photo_link)
        self.db.add(db_place)
        self.db.commit()
        self.db.refresh(db_place)
        return db_place

    def add_place_visit(self, trip_day_id: int, place_id: int, order: int) -> PlaceVisit:
        db_place_visit = PlaceVisit(trip_day_id=trip_day_id, place_id=place_id, order=order)
        self.db.add(db_place_visit)
        self.db.commit()
        self.db.refresh(db_place_visit)
        return db_place_visit

    def get_all_places(self) -> List[Place]:
        return self.db.query(Place).all()

    def get_place_by_id(self, place_id: int) -> Optional[Place]:
        return self.db.query(Place).filter(Place.id == place_id).first()

    def get_user_trips(self, user_id: int) -> List[Trip]:
        return self.db.query(Trip).filter(Trip.user_id == user_id).all()

    def get_trip_by_id(self, trip_id: int) -> Optional[Trip]:
        return self.db.query(Trip).filter(Trip.id == trip_id).first()

    def get_trip_days(self, trip_id: int) -> List[TripDay]:
        return self.db.query(TripDay).filter(TripDay.trip_id == trip_id).order_by(TripDay.day_number).all()

    def get_day_places(self, trip_day_id: int) -> List[PlaceVisit]:
        return self.db.query(PlaceVisit).filter(
            PlaceVisit.trip_day_id == trip_day_id
        ).order_by(PlaceVisit.order).all()

    def update_trip(self, trip_id: int, **kwargs) -> Optional[Trip]:
        trip = self.get_trip_by_id(trip_id)
        if trip:
            for key, value in kwargs.items():
                setattr(trip, key, value)
            self.db.commit()
            self.db.refresh(trip)
        return trip

    def delete_trip(self, trip_id: int) -> bool:
        trip = self.get_trip_by_id(trip_id)
        if trip:
            self.db.delete(trip)
            self.db.commit()
            return True
        return False

    def update_place(self, place_id: int, **kwargs) -> Optional[Place]:
        place = self.get_place_by_id(place_id)
        if place:
            for key, value in kwargs.items():
                setattr(place, key, value)
            self.db.commit()
            self.db.refresh(place)
        return place

    def delete_place(self, place_id: int) -> bool:
        place = self.get_place_by_id(place_id)
        if place:
            self.db.delete(place)
            self.db.commit()
            return True
        return False

    def update_trip_day(self, trip_day_id: int, **kwargs) -> Optional[TripDay]:
        trip_day = self.db.query(TripDay).filter(TripDay.id == trip_day_id).first()
        if trip_day:
            for key, value in kwargs.items():
                setattr(trip_day, key, value)
            self.db.commit()
            self.db.refresh(trip_day)
        return trip_day

    def delete_trip_day(self, trip_day_id: int) -> bool:
        trip_day = self.db.query(TripDay).filter(TripDay.id == trip_day_id).first()
        if trip_day:
            self.db.delete(trip_day)
            self.db.commit()
            return True
        return False

    def get_places_by_tag(self, db: Session, tag: str) -> List[Place]:
        """Получение мест по тегу"""
        return db.query(Place).filter(Place.tags.contains(tag)).all()

    def get_place_tags(self, db: Session, place_id: int) -> List[str]:
        """Получение тегов места"""
        place = self.get_place_by_id(db, place_id)
        if place and place.tags:
            return place.tags.split(',')
        return []