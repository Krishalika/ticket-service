import os

import stripe
from dotenv import load_dotenv
from fastapi import Header
import dotenv
from model.ticket_model import TicketModel
from utils.db_utils import load_db

db = load_db()
load_dotenv()

collection = db["tickets"]
stripe.api_key = "sk_test_51OPsooGpa94GP3zWQItoqSmPaZEiPxrtnFwvUuaPS7pdNhiVzeaRGxsoyx9cDpKnR0xRernroxYoOx2jqxNt510k00ykZnARwE"

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

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Flight Ticket',
                        },
                        'unit_amount': ticket.price * 100,  # Amount in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://website.com/success',  # success URL
                cancel_url='https://website.com/cancel',  # cancel URL
            )

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
