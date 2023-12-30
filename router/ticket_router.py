from fastapi import APIRouter, HTTPException

from model.ticket_model import TicketModel
from service.ticket_service import TicketService
from service.ticket_service import get_all_tickets

ticket_router = APIRouter()


@ticket_router.post("/ticket/purchase/")
async def purchase_ticket(ticket: TicketModel):
    """Purchase a ticket"""
    try:
        result = await TicketService.purchase_ticket(ticket)
        return result
    except Exception as e:
        # Handle specific exceptions if needed
        raise HTTPException(status_code=500, detail="Error occurred, please try again \n")


@ticket_router.get("/ticket/all")
async def get_all_purchased_tickets():
    """Get all tickets"""
    try:
        result = await get_all_tickets()
        return result
    except HTTPException as e:
        # Handle HTTP exceptions
        raise e
