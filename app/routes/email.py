from pydantic import BaseModel, Field, EmailStr
from fastapi import APIRouter, HTTPException, Query
from app.services.email_services import generate_email, send_mail
# from app.models.model import EmailRequest

class GenerationRequest(BaseModel):
    recipient_email: EmailStr
    recipient_phone: str
    company_name: str
    industry: str
    engagement_level: int
    objection: str
    insurance_company_name: str
    sender_name: str
    # sender_email: EmailStr

class EmailRequest(BaseModel):
    sender_email: EmailStr
    recipient_email: EmailStr
    subject: str
    generatedEmail: str



router = APIRouter()


@router.post("/email/generate")
def generate_cold_email(request: GenerationRequest):
    try:
        return generate_email( request.recipient_email,  
                    request.recipient_phone,
                    request.company_name,  
                    request.industry,
                    request.engagement_level,
                    request.objection,
                    request.insurance_company_name,
                    request.sender_name,
                    # request.sender_email 
                )
        # return "Success"
    except Exception as e:
        return {"message": f"Email generation failed: {e}"}
    


@router.post("/email/send")
def send_cold_email(request: EmailRequest):
    try:
        return send_mail(
            request.sender_email,
            request.recipient_email,
            request.subject, 
            request.generatedEmail
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email sending failed: {e}")
