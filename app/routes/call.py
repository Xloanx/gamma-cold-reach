from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field, EmailStr
from app.services.call_services import make_phone_call
# from app.models.model import CallRequest

class CallRequest(BaseModel):
    recipient_phone: str
    call_script: str

router = APIRouter()


@router.post("/call")
def send_cold_call(request: CallRequest):
    try:
        make_phone_call(
            request.recipient_phone,
            request.call_script
        )
        return "Success"
    except Exception as e:
        return "Failure"
    