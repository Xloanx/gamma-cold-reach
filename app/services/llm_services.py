# import pandas as pd
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableParallel
from langchain_groq import ChatGroq
from langchain.schema.output_parser import StrOutputParser
from config import groq_api_key
import json


from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
from config import groq_api_key

def generate_output(
        recipient_email,  
        recipient_phone,
        company_name,  
        industry,
        engagement_level,
        objection,
        insurance_company_name,
        sender_name
):
    """
    Generates a personalized cold email using LangChain and Groq Llama3-8B.
    """

     # Get industry-specific messaging
    industry_context = get_industry_context(industry)

    # Extract values to pass into PromptTemplate
    opening = industry_context.get("opening", "Stay ahead with industry-leading protection.")
    value_prop = industry_context.get("value_prop", "We provide comprehensive coverage tailored to your needs.")
    objection_handling = industry_context.get("objection_handling", "Our policies are designed to be flexible and affordable.")


    # Define the AI-powered prompt
    prompt_template = PromptTemplate(
        template="""
      You are an AI Cold Outreach Assistant for an insurance company. 
        Your task is to generate a **personalized cold email** and a **short cold call script** based on the prospect's details.

        **Industry-Specific Context:**
        - **Opening:** {opening}
        - **Value Proposition:** {value_prop}
        - **Objection Handling:** {objection_handling}


        **Input Data:**
        - Recipient Email: {recipient_email}
        - Recipient Phone: {recipient_phone}
        - Company Name: {company_name}
        - Industry: {industry}
        - Engagement Level: {engagement_level}
        - Potential Objection: {objection}
        - Insurance Company Name: {insurance_company_name}
        - Sender Name: {sender_name}

        **Cold Email Structure:**
        1. **[Opening]**: Mention a relevant industry trend or challenge.
        2. **[Value Proposition]**: Explain why {insurance_company_name} is the best solution.
        3. **[Objection Handling]**: Address the main concern ({objection}).
        4. **[Call-to-Action]**: Invite the recipient to book a call or respond.

        **Output (Strict JSON format):**
        {{
            "recipient_email": "{recipient_email}",
            "recipient_phone": "{recipient_phone}",
            "subject": "[Compelling subject line]",
            "email": "[Generated cold email content without the subject line]",
            "call_script": "[Short, effective cold call script]",
            "advise": "[Follow-up strategy]"
        }}
        """,
        input_variables=[
            "recipient_email", "recipient_phone", "company_name",
            "industry", "engagement_level", "objection",
            "insurance_company_name", "sender_name", "opening", "value_prop", "objection_handling"
        ]
    )

    # Initialize the LLM (Groq API - Llama3)
    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0.7,  # Balanced creativity
        max_tokens=1024,
        api_key=groq_api_key
    )

    # Define output parser
    parser = JsonOutputParser()

    # Create LangChain chain
    email_chain = prompt_template | llm | parser

    # Invoke the chain with input data
    response = email_chain.invoke({
        "recipient_email": recipient_email,
        "recipient_phone": recipient_phone,
        "company_name": company_name,
        "industry": industry,
        "engagement_level": engagement_level,
        "objection": objection,
        "insurance_company_name": insurance_company_name,
        "sender_name": sender_name,
        "opening": opening,
        "value_prop": value_prop,
        "objection_handling": objection_handling
    })

    return response



def generate_outreach_content(
        recipient_email,  
        recipient_phone,
        company_name,  
        industry,
        engagement_level,
        objection,
        insurance_company_name,
        sender_name
):
    """
    Generates both a cold email and a cold call script in parallel using LangChain.
    """

    # Get industry-specific messaging
    industry_context = get_industry_context(industry)

    # Email Generation Prompt
    email_prompt = PromptTemplate(
        template=f"""
        You are an AI-powered email assistant for {insurance_company_name}. 
        Generate a **personalized cold email** for {company_name} (Industry: {industry}).

        **Industry-Specific Context:**
        - **Opening:** {industry_context['opening']}
        - **Value Proposition:** {industry_context['value_prop']}
        - **Objection Handling:** {industry_context['objection_handling']}

        **Email Structure:**
        1. **Engaging opening** (Industry-specific)
        2. **Value proposition** (Why your insurance is useful)
        3. **Objection handling** ({objection})
        4. **Clear call to action (CTA)** (Schedule a call, etc.)

        **Output JSON:**
        {{
            "subject": "[Engaging subject line]",
            "email": "[Generated email text]",
            "advise": "[Follow-up strategy and recommendations]"
        }}
        """,
        input_variables=["company_name", "industry", "objection", "insurance_company_name", "sender_name"]
    )

    # Call Script Generation Prompt
    call_prompt = PromptTemplate(
        template=f"""
        You are a sales assistant generating cold call scripts for {insurance_company_name}.
        Write a **short, compelling** sales script for a call to {company_name} (Industry: {industry}).
        
        **Industry-Specific Context:**
        - **Opening:** {industry_context['opening']}
        - **Value Proposition:** {industry_context['value_prop']}
        - **Objection Handling:** {industry_context['objection_handling']}

        **Call Structure:**
        1. **Quick intro** ("Hi, I'm {sender_name} from {insurance_company_name}...")
        2. **Main benefit** (Industry-specific)
        3. **Handling objection** ({objection})
        4. **Clear call to action** (Book a call)

        **Output JSON:**
        {{
            "call_script": "[Generated call script]"
        }}
        """,
        input_variables=["company_name", "industry", "objection", "insurance_company_name", "sender_name"]
    )

    # Initialize the LLM (Groq API - Llama3)
    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0.7,
        max_tokens=1024,
        api_key=groq_api_key
    )

    # Define output parser
    parser = JsonOutputParser()

    # Create individual chains
    email_chain = email_prompt | llm | parser
    call_chain = call_prompt | llm | parser

    # Run both chains in parallel
    combined_chain = RunnableParallel(
        email=email_chain,
        call=call_chain
    )

    # Invoke the parallel chain
    response = combined_chain.invoke({
        "company_name": company_name,
        "industry": industry,
        "objection": objection,
        "insurance_company_name": insurance_company_name,
        "sender_name": sender_name
    })

    return response


def get_industry_context(industry):
    """
    Returns the correct industry-specific messaging style for the AI to use.
    """
    industry_styles = {
    "Tech": {
        "opening": "Tech innovation is rapidly evolving, and staying protected is key.",
        "value_prop": "Our insurance ensures your startup scales securely with risk protection.",
        "objection_handling": "Many tech startups think insurance is costly, but we offer flexible plans.",
    },
    "Finance": {
        "opening": "Financial security and compliance are the backbone of success.",
        "value_prop": "We help finance firms mitigate risks while maintaining compliance effortlessly.",
        "objection_handling": "ROI is key in finance, and our policies maximize returns while reducing risk.",
    },
    "Healthcare": {
        "opening": "Healthcare demands high compliance and patient data security.",
        "value_prop": "We provide tailored insurance for healthcare providers, ensuring compliance & efficiency.",
        "objection_handling": "Regulatory concerns? Our policies align with HIPAA and other healthcare standards.",
    },
    "Manufacturing": {
        "opening": "Supply chain disruptions and operational risks impact manufacturing.",
        "value_prop": "Our insurance covers machinery, workforce, and logistics to keep operations running.",
        "objection_handling": "We provide cost-effective coverage that prevents expensive production halts.",
    },
    "Retail": {
        "opening": "Retail businesses thrive on seamless operations and customer trust.",
        "value_prop": "We offer comprehensive coverage for inventory, employees, and liabilities.",
        "objection_handling": "Think insurance is too complex? Our plans simplify coverage at affordable rates.",
    },
    "Real Estate": {
        "opening": "Property investments need security against unforeseen losses.",
        "value_prop": "Our insurance protects assets, tenants, and investors for uninterrupted business.",
        "objection_handling": "Worried about high premiums? We customize policies to fit your portfolio size.",
    },
    "Education": {
        "opening": "Schools and institutions must safeguard students, staff, and facilities.",
        "value_prop": "We provide specialized policies covering liability, property, and cyber threats.",
        "objection_handling": "Budget constraints? Our solutions are designed for affordability and protection.",
    },
    "E-commerce": {
        "opening": "Online businesses face cyber threats and operational risks daily.",
        "value_prop": "We offer coverage for data breaches, lost shipments, and liability claims.",
        "objection_handling": "Insurance is often overlooked in e-commerce, but our plans are cost-effective.",
    },
    "Transportation & Logistics": {
        "opening": "Logistics companies must ensure supply chains remain uninterrupted.",
        "value_prop": "We cover fleet insurance, cargo protection, and driver liability risks.",
        "objection_handling": "Think insurance is expensive? We offer scalable plans based on fleet size.",
    },
    "Hospitality": {
        "opening": "The hospitality industry thrives on seamless guest experiences.",
        "value_prop": "We cover property damage, liability claims, and business interruptions.",
        "objection_handling": "Our policies protect hotels and restaurants while staying budget-friendly.",
    },
    "Construction": {
        "opening": "Construction projects face high risks, from delays to equipment damage.",
        "value_prop": "We provide builder’s risk insurance, liability coverage, and workers’ protection.",
        "objection_handling": "Worried about high premiums? We adjust plans to project size and duration.",
    },
    "Energy & Utilities": {
        "opening": "Energy providers operate in high-risk environments with costly assets.",
        "value_prop": "Our policies cover equipment failure, liability, and environmental risks.",
        "objection_handling": "We help energy firms mitigate risks while staying compliant with regulations.",
    },
    "Legal Services": {
        "opening": "Law firms must safeguard client data and maintain professional liability protection.",
        "value_prop": "We offer tailored policies to protect against malpractice claims and data breaches.",
        "objection_handling": "Our coverage is designed to meet the unique needs of legal professionals.",
    },
    "Marketing & Advertising": {
        "opening": "Marketing agencies handle high-stakes client campaigns and data security.",
        "value_prop": "Our policies protect agencies from liability claims and cyber threats.",
        "objection_handling": "We provide coverage without disrupting your advertising budget.",
    },
    "Agriculture": {
        "opening": "Farming and agribusinesses face unpredictable weather and market conditions.",
        "value_prop": "We offer crop insurance, livestock protection, and liability coverage.",
        "objection_handling": "Our affordable policies shield agribusinesses from unforeseen losses.",
    },
}

    
    # Default fallback if industry isn't explicitly handled
    return industry_styles.get(industry, {
        "opening": "Running a business comes with risks, and protection is crucial.",
        "value_prop": "We provide industry-leading insurance tailored to your business needs.",
        "objection_handling": "We understand concerns about cost, but our policies offer unmatched value.",
    })