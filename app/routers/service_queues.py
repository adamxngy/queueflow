from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.service_queue import ServiceQueueCreate, ServiceQueueRead
from app.services.service_queue_service import (
    create_service_queue,
    get_service_queues,
)


router = APIRouter(
    prefix="/service-queues",
    tags=["Service Queues"],
)


@router.post(
    "",
    response_model=ServiceQueueRead,
    status_code=status.HTTP_201_CREATED,
)
def create_queue(
    queue_data: ServiceQueueCreate,
    db: Session = Depends(get_db),
):
    return create_service_queue(db, queue_data)


@router.get(
    "",
    response_model=list[ServiceQueueRead],
)
def list_queues(
    db: Session = Depends(get_db),
):
    return get_service_queues(db)