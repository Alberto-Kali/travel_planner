from sqlalchemy.orm import Session
from app.db.crud import CRUDPlace
from app.models.trip import Place
import json

initial_places = [
    {
        "name": "Куршская коса",
        "tags": json.dumps(['природа', 'история']),
        "cords": json.dumps(['54.0002', '20.00001']),
        "description": "Национальный парк, расположенный на Куршской косе, представляет собой узкую полоску земли между Балтийским морем и Куршским заливом.",
        "photo_link": "kurshskaya_kosa.jpg",
        "rating": 10.0
    }
]

def init_places(db: Session):
    for place_data in initial_places:
        existing_place = db.query(Place).filter(Place.name == place_data["name"]).first()
        if not existing_place:
            db_place = Place(**place_data)
            db.add(db_place)
            db.commit()
            db.refresh(db_place)
