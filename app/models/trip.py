from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
import json

class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    tags = Column(String)
    cords = Column(String)
    description = Column(String)
    photo_link = Column(String)
    rating = Column(Float)

    @property
    def tags_list(self):
        return json.loads(self.tags) if self.tags else []

    @tags_list.setter 
    def tags_list(self, value):
        self.tags = json.dumps(value) if value else None

    @property
    def coordinates(self):
        return json.loads(self.cords) if self.cords else None

    @coordinates.setter
    def coordinates(self, value):
        self.cords = json.dumps(value) if value else None

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(String)
    start_date = Column(String)
    end_date = Column(String)

    user = relationship("User", back_populates="trips")
    days = relationship("TripDay", back_populates="trip")

class TripDay(Base):
    __tablename__ = "trip_days"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    day_number = Column(Integer)
    total_distance_km = Column(Float)
    total_time_hours = Column(Float)
    transport = Column(String)

    trip = relationship("Trip", back_populates="days")
    places = relationship("PlaceVisit", back_populates="trip_day")

class PlaceVisit(Base):
    __tablename__ = "place_visits"

    id = Column(Integer, primary_key=True, index=True)
    trip_day_id = Column(Integer, ForeignKey("trip_days.id"))
    place_id = Column(Integer, ForeignKey("places.id"))
    order = Column(Integer)

    trip_day = relationship("TripDay", back_populates="places")
    place = relationship("Place")
