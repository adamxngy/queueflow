from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.ticket import TicketCreate, TicketRead
from app.services.ticket_service import (
    call_next_ticket,
    complete_ticket,
    create_ticket_for_queue,
    get_tickets_for_queue,
)


router = APIRouter(
    prefix="/service-queues/{queue_id}/tickets",
    tags=["Tickets"],
)


@router.post(
    "",
    response_model=TicketRead,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(
    queue_id: int,
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
):
    return create_ticket_for_queue(db, queue_id, ticket_data)


@router.get(
    "",
    response_model=list[TicketRead],
)
def list_tickets(
    queue_id: int,
    db: Session = Depends(get_db),
):
    return get_tickets_for_queue(db, queue_id)


@router.post(
    "/call-next",
    response_model=TicketRead,
)
def call_next(
    queue_id: int,
    db: Session = Depends(get_db),
):
    return call_next_ticket(db, queue_id)


@router.post(
    "/{ticket_id}/complete",
    response_model=TicketRead,
)
def complete(
    queue_id: int,
    ticket_id: int,
    db: Session = Depends(get_db),
):
    return complete_ticket(db, queue_id, ticket_id)