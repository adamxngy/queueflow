from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.service_queue import ServiceQueue
from app.schemas.service_queue import ServiceQueueCreate


def create_service_queue(
    db: Session,
    queue_data: ServiceQueueCreate,
) -> ServiceQueue:
    existing_queue = db.scalar(
        select(ServiceQueue).where(ServiceQueue.name == queue_data.name)
    )

    if existing_queue:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Service queue with name '{queue_data.name}' already exists.",
        )

    service_queue = ServiceQueue(
        name=queue_data.name,
        active=queue_data.active,
    )

    db.add(service_queue)
    db.commit()
    db.refresh(service_queue)

    return service_queue


def get_service_queues(db: Session) -> list[ServiceQueue]:
    return list(
        db.scalars(
            select(ServiceQueue).order_by(ServiceQueue.id)
        )
    )