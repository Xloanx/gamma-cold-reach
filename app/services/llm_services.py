# import pandas as pd
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_together import ChatTogether
from langchain_groq import ChatGroq
from langchain.schema.output_parser import StrOutputParser
from config import groq_api_key
import json


def generate_mail_body(
        recipient_email,  
        recipient_phone,
        company_name,  
        industry,
        engagement_level,
        objection,
        insurance_company_name,
        sender_name
):

    prompt = """
    You are an AI-powered Cold Outreach Assistant for an insurance company specializing in personalized marketing. Your goal is to craft **highly engaging cold emails** and **concise, high-converting cold call scripts** tailored to prospects' industries, prior engagement levels, and potential objections. Additionally, you will provide strategic follow-up advice to further engage the client.

    ---

    ### **Task**  
    Given the following details, generate a JSON response containing:  

    1. `recipient_email`: The **email address of the recipient** (as provided in the input).  
    2. `recipient_phone`: The **phone number of the recipient** (as provided in the input).  
    3. `subject`: A compelling **email subject line** that grabs attention and encourages the recipient to open the email.  
    4. `email`: A **personalized cold email** that follows this structure:  
    - **[Opening sentence]**: Connect with their industry, a recent trend, or challenge.  
    - **[Value proposition]**: How your insurance solution helps companies in their industry.  
    - **[Objection handling]**: Address a common concern relevant to their industry.  
    - **[CTA]**: Suggest a **quick call, demo, or free consultation**.  

    5. `call_script`: A **short but effective cold call script** (under 100 words) that:  
    - Starts with a **brief introduction**.  
    - Highlights a **pain point** relevant to their industry.  
    - Presents the **key benefit of the insurance** in a single sentence.  
    - Handles a **likely objection** in one sentence.  
    - Ends with a **clear CTA** (e.g., booking a call, requesting more info).  

    6. `advise`: A **follow-up strategy** to keep the client engaged based on their industry and potential objection.  

    ---

    ### **Input**  
    - **Recipient Email**: {recipient_email}  
    - **Recipient Phone**: {recipient_phone}  
    - **Company Name**: {company_name}  
    - **Industry**: {industry}  
    - **Engagement Level**: {engagement_level}  
    - **Potential Objection**: {objection}  
    - **Insurance Company Name**: {insurance_company_name}  
    - **Sender Name**: {sender_name}  

    ---

    ###Note: The email is sent to {company_name} so the greeting at the beginning of the email should be attributed to {company_name}

    ---

    ### **Output Format (Strict JSON)**  
    {{
    "recipient_email": "{recipient_email}",
    "recipient_phone": "{recipient_phone}",
    "subject": "[Compelling subject line]",
    "email": "[Generated cold email]",
    "call_script": "[Short, high-impact cold call script]",
    "advise": "[Follow-up strategy and recommendations]"
    }}
    """  

    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0,
        max_tokens=1024,
        timeout=None,
        max_retries=2,
        api_key=groq_api_key
    )

    parser = JsonOutputParser()

    prompt_template = PromptTemplate(
    template=prompt,
    input_variables=[company_name, industry, engagement_level, objection],
    partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    first_chain = prompt_template | llm | parser

    response = first_chain.invoke({
    "company_name": company_name,
    "industry": industry,
    "engagement_level": engagement_level,
    "objection": objection,
    "insurance_company_name": insurance_company_name,
    "sender_name": sender_name,
    "recipient_email": recipient_email,
    "recipient_phone": recipient_phone
    })
    print(f"response \n:{response}")
    # return json.loads(response)
    return response