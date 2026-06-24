from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.service_queue import ServiceQueue


class TicketStatus(str, Enum):
    WAITING = "WAITING"
    CALLED = "CALLED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_name: Mapped[str] = mapped_column(nullable=False)

    status: Mapped[TicketStatus] = mapped_column(
        SQLAlchemyEnum(
            TicketStatus,
            name="ticket_status",
            native_enum=False,
            validate_strings=True,
        ),
        default=TicketStatus.WAITING,
        nullable=False,
    )

    service_queue_id: Mapped[int] = mapped_column(
        ForeignKey("service_queues.id"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    called_at: Mapped[datetime | None] = mapped_column(nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    service_queue: Mapped["ServiceQueue"] = relationship(
        back_populates="tickets",
    )