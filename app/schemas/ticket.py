from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.ticket import TicketStatus


class TicketCreate(BaseModel):
    customer_name: str = Field(
        min_length=1,
        max_length=100,
        examples=["Adam"],
    )

    @field_validator("customer_name")
    @classmethod
    def customer_name_must_not_be_blank(cls, value: str) -> str:
        stripped_value = value.strip()

        if not stripped_value:
            raise ValueError("Customer name must not be blank.")

        return stripped_value


class TicketRead(BaseModel):
    id: int
    customer_name: str
    status: TicketStatus
    service_queue_id: int
    created_at: datetime
    called_at: datetime | None
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)