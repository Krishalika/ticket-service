import stripe
from fastapi import Header

from model.ticket_model import TicketModel
from utils.db_utils import load_db

db = load_db()
collection = db["tickets"]


async def get_all_tickets():
    tickets = await collection.find().to_list(length=None)
    for obj in tickets:
        obj.pop('_id', None)
    return tickets


class TicketService:

    @staticmethod
    async def purchase_ticket(ticket: TicketModel, authorization: str = Header(...)):
        try:
            ticket_data = ticket.model_dump()
            # Create a charge using the Stripe API
            # TODO Add Stripe payment logic

            # If the payment is successful, save ticket details to MongoDB
            result = await collection.insert_one(ticket_data)
            ticket.ticket_id = str(result.inserted_id)

            # Return a success response
            return {"status": "success", "message": "Purchase successful", "ticket": ticket.model_dump()}

        except stripe.error.CardError as e:
            # Handle specific Stripe errors
            return {"status": "error", "message": str(e)}
        except stripe.error.StripeError as e:
            # Handle generic Stripe errors
            return {"status": "error", "message": "Something went wrong. Please try again later."}
