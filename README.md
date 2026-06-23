# QueueFlow

QueueFlow is a digital queue management system for physical service businesses such as clinics, banks, government offices, barbers, and service centers.

Customers can join a queue online, receive a ticket, wait digitally, and get called when it is their turn. Staff members can manage queues from a dashboard, call the next ticket, complete tickets, and later view live analytics.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker Compose
- Pydantic
- Jinja2 templates
- Pytest

## Current Status

Initial FastAPI project setup.

## Planned MVP Features

- Create a service queue
- Create a ticket for a queue
- List tickets for a queue
- Call the next waiting ticket
- Complete a called ticket
- Ticket statuses: WAITING, CALLED, COMPLETED, CANCELLED
- Clean error handling
- Simple staff dashboard UI

## Running Locally

Create and activate a virtual environment:

```bash
python -m venv .venv 
