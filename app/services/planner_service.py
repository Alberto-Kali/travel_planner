from typing import Dict, List, Optional
from app.services.giga_service import GigaAPI
from app.services.db_service import DBService
from app.models.trip import Trip
from app.models.user import User

class PlannerService:
    def __init__(self):
        self.giga_api = GigaAPI()
        self.conversation_states = {}

    async def start_planning(self, user_id: str) -> Dict:
        """Начало планирования поездки"""
        initial_prompt = self._get_initial_prompt()
        self.conversation_states[user_id] = {
            "stage": "initial",
            "history": [{"role": "system", "content": initial_prompt}]
        }
        return {"message": "Давайте спланируем вашу поездку. Сколько дней вы хотите путешествовать?"}

    async def process_message(self, user_id: str, message: str, db_service: DBService) -> Dict:
        """Обработка сообщения от пользователя"""
        if user_id not in self.conversation_states:
            return await self.start_planning(user_id)

        state = self.conversation_states[user_id]
        state["history"].append({"role": "user", "content": message})

        response = await self.giga_api.get_completion(state["history"])
        assistant_message = response['choices'][0]["message"]['content']

        state["history"].append({"role": "assistant", "content": assistant_message})

        # Обработка различных этапов планирования
        if state["stage"] == "initial":
            return await self._process_initial_stage(user_id, assistant_message, db_service)
        elif state["stage"] == "route_planning":
            return await self._process_route_planning(user_id, assistant_message, db_service)

        return {"message": assistant_message}

    def _get_initial_prompt(self) -> str:
        return """Ты профессиональный планировщик путешествий по Калининградской области. 
        Твоя задача - помочь пользователю составить оптимальный маршрут путешествия.
        Спроси у пользователя:
        1. Количество дней путешествия
        2. Предпочтения по местам (природа, история, архитектура, etc.)
        3. Предпочитаемый вид транспорта
        На основе этой информации предложи маршрут."""

    async def _process_initial_stage(self, user_id: str, message: str, db_service: DBService) -> Dict:
        """Обработка начального этапа планирования"""
        # Здес добавить логику создания нового Trip
        # Например:
        # new_trip = db_service.create_trip(
        #     user_id=user_id,
        #     title="Новое путешествие",
        #     description="План путешествия",
        #     start_date="2024-01-01",
        #     end_date="2024-01-05"
        # )
        
        self.conversation_states[user_id]["stage"] = "route_planning"
        return {"message": message}

    async def _process_route_planning(self, user_id: str, message: str, db_service: DBService) -> Dict:
        """Обработка этапа планирования маршрута"""
        # Здесь добавить логику создания TripDay и PlaceVisit
        # Например:
        # trip_day = db_service.add_trip_day(
        #     trip_id=trip_id,
        #     day_number=1,
        #     total_distance_km=100.0,
        #     total_time_hours=8.0,
        #     transport="Car"
        # )
        return {"message": message}

    async def save_trip_plan(self, user_id: str, db_service: DBService) -> Dict:
        """Сохранение финального плана путешествия"""
        if user_id not in self.conversation_states:
            raise ValueError("No active planning session")

        # Здесь добавить логику финализации и сохранения плана
        # Например:
        # final_trip = db_service.get_trip_by_id(trip_id)
        # db_service.update_trip(trip_id, status="confirmed")

        return {"message": "План путешествия успешно сохранен"}

    def get_available_places(self, db_service: DBService) -> List[Dict]:
        """Получение списка доступных мест для посещения"""
        places = db_service.get_all_places()
        return [{"id": place.id, "name": place.name, "description": place.description} for place in places]

    def get_trip_details(self, trip_id: int, db_service: DBService) -> Dict:
        """Получение детальной информации о путешествии"""
        trip = db_service.get_trip_by_id(trip_id)
        if not trip:
            raise ValueError("Trip not found")

        days = db_service.get_trip_days(trip_id)
        trip_days = []
        for day in days:
            places = db_service.get_day_places(day.id)
            trip_days.append({
                "day_number": day.day_number,
                "total_distance": day.total_distance_km,
                "total_time": day.total_time_hours,
                "transport": day.transport,
                "places": [{"id": pv.place_id, "order": pv.order} for pv in places]
            })

        return {
            "id": trip.id,
            "title": trip.title,
            "description": trip.description,
            "start_date": trip.start_date,
            "end_date": trip.end_date,
            "days": trip_days
        }

    def get_places_by_tags(self, tags: List[str], db_service: DBService) -> List[Dict]:
        """Получение мест по тегам"""
        places = db_service.get_all_places()
        filtered_places = []
        
        for place in places:
            place_tags = place.tags.split(',')
            if any(tag in place_tags for tag in tags):
                filtered_places.append({
                    "id": place.id,
                    "name": place.name,
                    "description": place.description,
                    "tags": place_tags,
                    "rating": place.rathing,
                    "coordinates": place.cords
                })
        
        return filtered_places

    def get_available_tags(self, db_service: DBService) -> List[str]:
        """Получение списка всех доступных тегов"""
        places = db_service.get_all_places()
        tags_set = set()
        
        for place in places:
            place_tags = place.tags.split(',')
            tags_set.update(place_tags)
        
        return list(tags_set)