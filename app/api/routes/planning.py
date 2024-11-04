from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from pydantic import BaseModel
from app.services.planner_service import PlannerService
from app.core.security import get_current_user
from app.models.user import User
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/planning", tags=["planning"])

class MessageRequest(BaseModel):
    message: str

@router.post("/start")
async def start_planning(
    current_user: User = Depends(get_current_user),
    planner: PlannerService = Depends(),
    db: Session = Depends(get_db)
) -> Dict:
    """Начало планирования поездки"""
    return await planner.start_planning(str(current_user.id), db)

@router.post("/message")
async def process_message(
    request: MessageRequest,
    current_user: User = Depends(get_current_user),
    planner: PlannerService = Depends(),
    db: Session = Depends(get_db)
) -> Dict:
    """Обработка сообщения в процессе планирования"""
    return await planner.process_message(str(current_user.id), request.message, db)

@router.get("/status")
async def get_planning_status(
    current_user: User = Depends(get_current_user),
    planner: PlannerService = Depends()
) -> Dict:
    """Получение текущего статуса планирования"""
    return {"status": "planning", "stage": "initial"}

@router.post("/save")
async def save_trip_plan(
    current_user: User = Depends(get_current_user),
    planner: PlannerService = Depends(),
    db: Session = Depends(get_db)
) -> Dict:
    """Сохранение финального плана путешествия"""
    return await planner.save_trip_plan(str(current_user.id), db)

@router.get("/places")
async def get_available_places(
    current_user: User = Depends(get_current_user),
    planner: PlannerService = Depends(),
    db: Session = Depends(get_db)
) -> Dict:
    """Получение списка доступных мест для посещения"""
    places = planner.get_available_places(db)
    return {"places": places}

@router.get("/trip/{trip_id}")
async def get_trip_details(
    trip_id: int,
    current_user: User = Depends(get_current_user),
    planner: PlannerService = Depends(),
    db: Session = Depends(get_db)
) -> Dict:
    """Получение детальной информации о путешествии"""
    return planner.get_trip_details(trip_id, db)

@router.get("/places/tags")
async def get_places_by_tags(
    tags: str,
    current_user: User = Depends(get_current_user),
    planner: PlannerService = Depends(),
    db: Session = Depends(get_db)
) -> Dict:
    """Получение мест по тегам"""
    tag_list = tags.split(',')
    places = planner.get_places_by_tags(tag_list, db)
    return {"places": places}

@router.get("/tags")
async def get_available_tags(
    current_user: User = Depends(get_current_user),
    planner: PlannerService = Depends(),
    db: Session = Depends(get_db)
) -> Dict:
    """Получение списка всех доступных тегов"""
    tags = planner.get_available_tags(db)
    return {"tags": tags}