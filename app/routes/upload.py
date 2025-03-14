from fastapi import APIRouter,UploadFile, File, BackgroundTasks, HTTPException, Form
import os
import pandas as pd
from pydantic import BaseModel
from fastapi.responses import FileResponse
from app.services.upload_services import process_campaign
from logging_config import logging



class CampaignRequest(BaseModel):
    insurance_company_name: str
    sender_name: str
    sender_email: str

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


router = APIRouter()


# Configure logging
# logging.basicConfig(
#     filename="campaign_log.log",  # Log file
#     level=logging.INFO,           # Log level
#     format="%(asctime)s - %(levelname)s - %(message)s"  # Log format
# )

@router.post("/upload")
async def upload_file(
    sender_email: str = Form(...),
    insurance_company_name: str = Form(...),
    sender_name: str = Form(...),
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    try:
        logging.info(f"Processing file: {file.filename}")

        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided.")
        
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        try:
            with open(file_path, "wb") as f:
                f.write(file.file.read())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

        # Read File Content
        try:
            if file.filename.endswith(".csv"):
                df = pd.read_csv(file_path)
            elif file.filename.endswith(".xlsx"):
                df = pd.read_excel(file_path)
            else:
                logging.error("Invalid file format.")
                raise HTTPException(status_code=400, detail="Invalid file format. Only CSV or Excel allowed.")
        except Exception as e:
            logging.exception("Error reading file")
            raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

        # Expected columns
        expected_columns = {"company_name", "industry", "recipient_email", "recipient_phone", "objection", "engagement_level"}
        if not expected_columns.issubset(df.columns):
            logging.error("Invalid CSV format. Missing required columns.")
            raise HTTPException(
                status_code=400,
                detail="Invalid CSV format. Required columns: company_name, industry, recipient_email, recipient_phone, objection, engagement_level"
            )

        # Background task to process emails
        try:
            logging.info(f"Starting background task for {insurance_company_name}")
            background_tasks.add_task(process_campaign, sender_email, insurance_company_name, sender_name, df, file.filename)
        except Exception as e:
            logging.exception("Error adding background task")
            raise HTTPException(status_code=500, detail=f"Error adding background task: {str(e)}")
        logging.info("File uploaded successfully. Campaign processing started.")
        return {"message": "File uploaded successfully, please wait emails are being sent in the background."}

    except HTTPException as http_exc:
        raise http_exc  # Re-raise known HTTP errors

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/download/{filename}")
async def download_report(filename: str):
    try:
        if not filename:
            raise HTTPException(status_code=400, detail="Filename is required.")

        file_path = os.path.join(UPLOAD_DIR, f"report_{filename}")

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found.")

        return FileResponse(file_path, media_type="text/csv", filename=f"Campaign_Report.csv")

    except HTTPException as http_exc:
        raise http_exc  # Re-raise known HTTP errors

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
