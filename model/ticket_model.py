from typing import Optional

from pydantic import BaseModel


class CardModel(BaseModel):
    number: str
    exp_month: str
    exp_year: str
    cvc: str


class TicketModel(BaseModel):
    flight_id: str
    passenger_email: str
    passenger_name: str
    price: int
    card: CardModel
    ticket_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "flight_id": "FL123",
                "passenger_email": "john.doe@example.com",
                "passenger_name": "John Doe",
                "price": 100,
                "card": {
                    "number": "4242424242424242",
                    "exp_month": "12",
                    "exp_year": "2024",
                    "cvc": "123"
                },
                "ticket_id": "5f4adc0a609a1e2b7d66c6c0"
            }
        }


# Example usage
ticket_data = {
    "flight_id": "FL123",
    "passenger_email": "john.doe@example.com",
    "passenger_name": "John Doe",
    "price": 100,
    "card": {
        "number": "4242424242424242",
        "exp_month": "12",
        "exp_year": "2024",
        "cvc": "123"
    },
    "ticket_id": "5f4adc0a609a1e2b7d66c6c0"
}

ticket_instance = TicketModel(**ticket_data)
