from fastapi import HTTPException
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from config import account_sid, auth_token, twilio_number

def make_phone_call(recipient_phone, call_script):
    """
    Makes a phone call to the recipient and speaks the script using Twilio.
    
    Parameters:
        recipent_phone (str): Recipient's phone number in E.164 format (e.g., "+1234567890").
        call_script (str): The text to be spoken during the call.
        twilio_number (str): Your Twilio phone number (E.164 format).
        account_sid (str): Twilio account SID.
        auth_token (str): Twilio authentication token.
    """

    if not recipient_phone:
        raise HTTPException(status_code=400, detail="Receiver number is required")
    
    # Initialize Twilio client
    client = Client(account_sid, auth_token)
    
    # Create TwiML (Telephony Markup Language) to define the call behavior
    twiml_response = VoiceResponse()
    twiml_response.say(call_script, voice='alice')  # 'alice' is a natural-sounding voice
    
    try:
        # Initiate the call
        call = client.calls.create(
            twiml=twiml_response.to_xml(),
            from_=twilio_number,
            to=recipient_phone
        )
        print(f"Call initiated! Call SID: {call.sid}")
        return {"message": "Call initiated", "call_sid": call.sid}
    except Exception as e:
        print(f"Failed to make call: {e}")
        return {f"Failed to make call: {e}"}