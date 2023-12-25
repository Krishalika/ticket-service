from fastapi import FastAPI

from router.ticket_router import ticket_router

# stripe.api_key = "sk_test_51OPsooGpa94GP3zWQItoqSmPaZEiPxrtnFwvUuaPS7pdNhiVzeaRGxsoyx9cDpKnR0xRernroxYoOx2jqxNt510k00ykZnARwE"

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

app.include_router(ticket_router, prefix="/api/v1", tags=["ticket"])
