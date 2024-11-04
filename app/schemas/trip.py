from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class PlaceBase(BaseModel):
    name: str
    description: str
    photo_link: str

class PlaceCreate(PlaceBase):
    pass

class Place(PlaceBase):
    id: int

    class Config:
        from_attributes = True

class TripBase(BaseModel):
    title: str
    description: str
    start_date: str
    end_date: str

class TripCreate(TripBase):
    pass

class Trip(TripBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True