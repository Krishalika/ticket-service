import stripe
from bson import ObjectId
from fastapi import HTTPException, Header

from model.ticket_model import TicketModel
from utils.db_utils import load_db

db = load_db()
collection = db["tickets"]


async def get_all_tickets():
    tickets = await collection.find().to_list(length=None)
    for obj in tickets:
        obj.pop('_id', None)
    return tickets


async def update_ticket(ticket_id: str, ticket: TicketModel):
    object_id = ObjectId(ticket_id)

    # Check if the ticket exists
    existing_ticket = await collection.find_one({"_id": object_id})
    if existing_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Update the ticket in the MongoDB collection
    await collection.update_one({"_id": object_id}, {"$set": ticket.model_dump()})

    # You may want to return the updated ticket or a success message
    updated_ticket = await collection.find_one({"_id": object_id})
    updated_ticket.pop('_id', None)
    return {"message": "Ticket updated successfully", "updated_ticket": updated_ticket}


async def delete_ticket(ticket_id: str):
    """
    Delete a ticket by ID
    :param ticket_id:
    :return:
    """
    object_id = ObjectId(ticket_id)

    # Check if the ticket exists
    existing_ticket = await collection.find_one({"_id": object_id})
    if existing_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Delete the ticket from the MongoDB collection
    await collection.delete_one({"_id": object_id})
    return {"message": "Ticket deleted successfully"}


async def get_ticket_by_id(ticket_id: str) -> dict:
    if not ObjectId.is_valid(ticket_id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

    ticket = await collection.find_one({"_id": ObjectId(ticket_id)})
    if ticket:
        return {"status": "success", "ticket": TicketModel(**ticket)}
    else:
        raise HTTPException(status_code=404, detail="Ticket not found")


class TicketService:

    @staticmethod
    async def purchase_ticket(ticket: TicketModel, authorization: str = Header(...)):
        try:
            # Assuming you have a validation method for the TicketModel
            ticket_data = ticket.model_dump()
            # Create a charge using the Stripe API
            # Add your Stripe payment logic here...

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
