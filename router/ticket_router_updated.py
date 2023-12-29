from fastapi import APIRouter, HTTPException

from model.ticket_model import TicketModel
from service.ticket_service_updated import TicketService
from service.ticket_service_updated import get_ticket_by_id, get_all_tickets, update_ticket, delete_ticket

ticket_router = APIRouter()


@ticket_router.post("/ticket/purchase/")
async def purchase_ticket(ticket: TicketModel):
    """Purchase a ticket"""
    try:
        result = await TicketService.purchase_ticket(ticket)
        return result
    except Exception as e:
        # Handle specific exceptions if needed
        raise HTTPException(status_code=500, detail="Internal Server Error")


@ticket_router.get("/ticket/details/{ticket_id}")
async def get_one_ticket_by_id(ticket_id: str):
    try:
        result = await get_ticket_by_id(ticket_id)
        return result
    except HTTPException as e:
        # Handle HTTP exceptions
        raise e


@ticket_router.get("/ticket/all")
async def get_all_purchased_tickets():
    """Get all tickets"""
    try:
        result = await get_all_tickets()
        return result
    except HTTPException as e:
        # Handle HTTP exceptions
        raise e


@ticket_router.put("/ticket/update/{ticket_id}")
async def update_ticket(ticket_id: str, ticket: TicketModel):
    """Update a ticket by ID"""
    try:
        result = await update_ticket(ticket)
        return result
    except HTTPException as e:
        # Handle HTTP exceptions
        raise e


@ticket_router.delete("/ticket/delete/{ticket_id}")
async def delete_ticket(ticket_id: str):
    """Delete a ticket by ID"""
    try:
        result = await delete_ticket(ticket_id)
        return result
    except HTTPException as e:
        # Handle HTTP exceptions
        raise e
