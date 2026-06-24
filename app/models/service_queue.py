from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.ticket import Ticket


class ServiceQueue(Base):
    __tablename__ = "service_queues"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="service_queue",
        cascade="all, delete-orphan",
    )