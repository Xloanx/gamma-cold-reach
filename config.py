from dotenv import load_dotenv
import os

load_dotenv()

account_sid=os.getenv("ACCOUNT_SID")
auth_token=os.getenv("AUTH_TOKEN")
twilio_number=os.getenv("TWILIO_NUMBER")
sender_password=os.getenv("SENDER_PASSWORD")
groq_api_key=os.getenv("GROQ_API_KEY")