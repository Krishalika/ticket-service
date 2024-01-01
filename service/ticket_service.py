import stripe
from dotenv import load_dotenv
from fastapi import Header, HTTPException

from model.ticket_model import TicketModel
from utils.utils import load_db

db = load_db()
load_dotenv()

collection = db["tickets"]
stripe.api_key = "pk_test_51OPsooGpa94GP3zWWg0F34h1g2axLfPNPro2f40q1v3KYcgJV1WjXzzqeu6xqkYrZcoKFa6YeijG2nONwgwM70aP00RA6MTv9E"


async def get_all_tickets():
    tickets = await collection.find().to_list(length=None)
    for obj in tickets:
        obj.pop('_id', None)
    return tickets


class TicketService:

    @staticmethod
    async def purchase_ticket(ticket: TicketModel, authorization: str = Header(...)):
        try:
            try:
                card_token = stripe.Token.create(
                    card={
                        "number": ticket.card.number,
                        "exp_month": ticket.card.exp_month,
                        "exp_year": ticket.card.exp_year,
                        "cvc": ticket.card.cvc,
                    },
                )
            except Exception as e:
                error_message = f"Incorrect card details, please try again. Details: {e.args[0]}"
                return error_message
            stripe.api_key = "sk_test_51OPsooGpa94GP3zWQItoqSmPaZEiPxrtnFwvUuaPS7pdNhiVzeaRGxsoyx9cDpKnR0xRernroxYoOx2jqxNt510k00ykZnARwE"

            print("Card token:", card_token)

            # Create a Checkout Session
            stripe.checkout.Session.create(
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
            ticket_data = ticket.dict()
            ticket_data.pop('card', None)
            result = await collection.insert_one(ticket_data)
            ticket.ticket_id = str(result.inserted_id)

            # Return a success response
            return {"status": "success", "message": "Purchase successful"}

        except stripe.error.CardError as e:
            # Handle specific Stripe errors
            raise HTTPException(status_code=400, detail={"status": "error", "message": str(e)})
        except stripe.error.StripeError as e:
            # return e
            # Handle generic Stripe errors
            raise HTTPException(status_code=500,
                                detail={"status": "error",
                                        "message": "Something went wrong. Please try again later." + str(e)})
