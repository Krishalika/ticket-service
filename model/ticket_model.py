from typing import Optional

from pydantic import BaseModel

class TicketModel(BaseModel):
    flight_id: str
    passenger_email: str
    passenger_name: str
    price: int
    card_details: str
    ticket_id: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "flight_id": "FL123",
                "passenger_email": "john.doe@example.com",
                "passenger_name": "John Doe",
                "price": 100,
                "card_details": "4242424242424242",
                "ticket_id": "5f4adc0a609a1e2b7d66c6c0"
            }
        }

