from pydantic import BaseModel, ConfigDict, Field, field_validator


class ServiceQueueCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
        examples=["General Practice"],
    )
    active: bool = True

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        stripped_value = value.strip()

        if not stripped_value:
            raise ValueError("Queue name must not be blank.")

        return stripped_value


class ServiceQueueRead(BaseModel):
    id: int
    name: str
    active: bool

    model_config = ConfigDict(from_attributes=True)