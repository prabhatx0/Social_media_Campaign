import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_llm():
    """Initializes and returns the ChatOpenAI model."""
    return ChatOpenAI(temperature=0.7, model_name="gpt-4o", openai_api_key=os.getenv("OPENAI_API_KEY"))

def analyze_text(scraped_text: str) -> str:
    """
    Analyzes scraped text to extract key themes, value propositions, and statistics.

    Args:
        scraped_text: The text content from the webpage.

    Returns:
        A structured analysis of the text.
    """
    if not scraped_text:
        logging.warning("Analysis skipped: input text is empty.")
        return ""

    logging.info("Starting text analysis...")

    analysis_template = """
    You are an expert marketing analyst. Your task is to analyze the following text from a product announcement or blog post and extract key information for a social media campaign.

    Please extract the following:
    1.  **Core Theme/Message**: What is the single most important message of this text?
    2.  **Key Value Propositions**: List 3-5 unique benefits or features highlighted. What problems do they solve for the user?
    3.  **Target Audience**: Who is this announcement for? (e.g., developers, marketers, general consumers).
    4.  **Key Statistics or Data Points**: Pull out any numbers, percentages, or concrete data mentioned.
    5.  **Tone of Voice**: Describe the tone of the original text (e.g., formal, casual, technical, enthusiastic).

    Provide the output in a clear, structured format.

    ---
    TEXT TO ANALYZE:
    {text}
    ---

    ANALYSIS:
    """

    prompt = ChatPromptTemplate.from_template(analysis_template)
    llm = get_llm()
    
    analysis_chain = prompt | llm | StrOutputParser()
    
    try:
        # Truncate text to avoid exceeding token limits, focusing on the most relevant part
        max_length = 15000  # Approx. 4k tokens
        truncated_text = scraped_text[:max_length]

        response = analysis_chain.invoke({"text": truncated_text})
        logging.info("Successfully completed text analysis.")
        return response
    except Exception as e:
        logging.error(f"An error occurred during text analysis: {e}")
        return "Error: Could not analyze the text."
