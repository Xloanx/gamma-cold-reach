from fastapi import HTTPException
from email.message import EmailMessage
import smtplib
import ssl
from config import sender_password
from app.services.llm_services import generate_output, generate_outreach_content

def generate_email(
        recipient_email,  
        recipient_phone,
        company_name,  
        industry,
        engagement_level,
        objection,
        insurance_company_name,
        sender_name,
        ):
    """
    Sends an email using the provided details and SMTP server (e.g., Gmail).
    
    Parameters:
    - subject (str): Email subject
    - recipient (str): Recipient email address
    - body (str): Email body content
    - sender_email (str): Sender's email address (requires SMTP access)
    - sender_password (str): Sender's email password or app-specific password
    """
    return generate_output(recipient_email,  
                recipient_phone,
                company_name,  
                industry,
                engagement_level,
                objection,
                insurance_company_name,
                sender_name)



def send_mail(sender_email, recipient_email, subject, generatedEmail):
    # Create the email message
    msg = EmailMessage()
    msg.set_content(generatedEmail)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Set up SSL context and SMTP server
    context = ssl.create_default_context()
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Email sent successfully!")
        return {"message": "Email sent successfully!"}
    except smtplib.SMTPAuthenticationError:
        raise HTTPException(status_code=401, detail="SMTP Authentication Error: Check email/password.")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")
