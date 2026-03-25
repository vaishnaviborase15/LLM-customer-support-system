from pydantic import BaseModel

class Ticket(BaseModel):
    ticket_id: int
    product: str
    ticket_type: str
    priority: str
    sentiment: str
    response: str

    class Config:
        from_attributes = True