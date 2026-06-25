from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.service_queue import ServiceQueue
from app.models.ticket import Ticket, TicketStatus
from app.schemas.ticket import TicketCreate


def get_queue_or_404(db: Session, queue_id: int) -> ServiceQueue:
    service_queue = db.get(ServiceQueue, queue_id)

    if service_queue is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service queue with id {queue_id} was not found.",
        )

    return service_queue


def get_ticket_or_404(
    db: Session,
    queue_id: int,
    ticket_id: int,
) -> Ticket:
    ticket = db.get(Ticket, ticket_id)

    if ticket is None or ticket.service_queue_id != queue_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with id {ticket_id} was not found in service queue {queue_id}.",
        )

    return ticket


def create_ticket_for_queue(
    db: Session,
    queue_id: int,
    ticket_data: TicketCreate,
) -> Ticket:
    service_queue = get_queue_or_404(db, queue_id)

    if not service_queue.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Service queue with id {queue_id} is not active.",
        )

    ticket = Ticket(
        customer_name=ticket_data.customer_name,
        status=TicketStatus.WAITING,
        service_queue_id=queue_id,
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


def get_tickets_for_queue(
    db: Session,
    queue_id: int,
) -> list[Ticket]:
    get_queue_or_404(db, queue_id)

    return list(
        db.scalars(
            select(Ticket)
            .where(Ticket.service_queue_id == queue_id)
            .order_by(Ticket.created_at, Ticket.id)
        )
    )


def call_next_ticket(
    db: Session,
    queue_id: int,
) -> Ticket:
    get_queue_or_404(db, queue_id)

    next_ticket = db.scalar(
        select(Ticket)
        .where(
            Ticket.service_queue_id == queue_id,
            Ticket.status == TicketStatus.WAITING,
        )
        .order_by(Ticket.created_at, Ticket.id)
        .with_for_update()
    )

    if next_ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No waiting tickets found for service queue {queue_id}.",
        )

    next_ticket.status = TicketStatus.CALLED
    next_ticket.called_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(next_ticket)

    return next_ticket


def complete_ticket(
    db: Session,
    queue_id: int,
    ticket_id: int,
) -> Ticket:
    ticket = get_ticket_or_404(db, queue_id, ticket_id)

    if ticket.status != TicketStatus.CALLED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only CALLED tickets can be completed.",
        )

    ticket.status = TicketStatus.COMPLETED
    ticket.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(ticket)

    return ticket