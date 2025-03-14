import os
import csv
from app.services.llm_services import generate_output
from app.services.email_services import send_mail
from logging_config import logging

UPLOAD_DIR = "uploads"



# Configure Logging
# logging.basicConfig(
#     filename="campaign_log.log",  # Log file
#     level=logging.INFO,  # Log level
#     format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
#     handlers=[logging.FileHandler("campaign_log.log"), logging.StreamHandler()]  # Save to file & show in terminal
# )

def process_campaign(sender_email, insurance_company_name, sender_name, df, filename):
    try:
        logging.info(f"Starting campaign processing for {insurance_company_name} - File: {filename}")

        if df.empty:
            logging.error("The provided DataFrame is empty.")
            raise ValueError("The provided DataFrame is empty.")
        
        results = []
        output_file = os.path.join(UPLOAD_DIR, f"report_{filename}.csv")

        for index, row in df.iterrows():
            try:
                company_name = row.get("company_name")
                recipient_email = row.get("recipient_email")
                industry = row.get("industry")
                recipient_phone = row.get("recipient_phone")
                objection = row.get("objection")
                engagement_level = row.get("engagement_level")
                generatedEmail =""
                subject = ""
                if not company_name or not recipient_email or not industry:
                    logging.warning(f"Missing required data in row {index}: {row}")
                    raise ValueError(f"Missing required data in row {index}: {row}")

                message = generate_output(recipient_email, recipient_phone, company_name, industry, 
                                          engagement_level, objection, insurance_company_name, sender_name)
                generatedEmail = message['email']
                subject = message['subject']
                email_sent = send_mail(sender_email, recipient_email, subject, generatedEmail)
                status = "Sent" if email_sent else "Failed"
                logging.info(f"Email {status} to {recipient_email} for {company_name}")
                results.append([company_name, recipient_email, message, "Sent" if email_sent else "Failed"])
            
            except Exception as e:
                logging.error(f"Error processing row {index}: {str(e)}")
                results.append([company_name, recipient_email, "Error generating message", f"Failed: {str(e)}"])
                continue  # Skip to the next row if an error occurs

        # Save Results
        try:
            with open(output_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Company", "Email", "Message", "Status"])
                writer.writerows(results)
            logging.info(f"Campaign report saved successfully: {output_file}")
        except Exception as e:
            logging.critical(f"Error saving report to {output_file}: {str(e)}")
            raise IOError(f"Error saving report to {output_file}: {str(e)}")

    except Exception as e:
        logging.critical(f"Error processing campaign: {str(e)}")
        raise RuntimeError(f"Error processing campaign: {str(e)}")



