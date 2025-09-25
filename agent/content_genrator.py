import os
import json
import logging
from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_llm():
    """Initializes and returns the ChatOpenAI model."""
    return ChatOpenAI(temperature=0.8, model_name="gpt-4o", openai_api_key=os.getenv("OPENAI_API_KEY"))

def generate_campaign_content(analysis: str, url: str) -> list:
    """
    Generates a 7-day social media campaign based on the text analysis.

    Args:
        analysis: The structured analysis from the nlp module.
        url: The source URL to include in the posts.

    Returns:
        A list of dictionaries, where each dictionary represents a social media post.
    """
    if not analysis or "Error" in analysis:
        logging.warning("Content generation skipped due to invalid analysis.")
        return []

    logging.info("Starting social media content generation...")

    generation_template = """
    You are a world-class social media strategist. Based on the following analysis of a blog post/product announcement, create a 7-day social media campaign.

    **Objective**: Generate excitement and drive traffic to the source URL.
    **Source URL**: {url}

    **Instructions**:
    1.  Create **5-7 posts for Twitter (X)**.
        - Tone: Catchy, concise, and engaging. Use relevant hashtags.
        - Format: Short sentences, questions, and strong calls to action. Each must include the {url}.
    2.  Create **5-7 posts for LinkedIn**.
        - Tone: Professional, informative, and value-oriented.
        - Format: Well-structured posts that explain the "why" and encourage professional discussion. Each must include the {url}.
    3.  Schedule the posts over 7 days, starting from tomorrow.
    4.  Return the output as a single JSON array of objects. Each object must have the following keys: "platform" (either "Twitter" or "LinkedIn"), "content" (the post text), and "scheduled_date" (in "YYYY-MM-DD" format).

    **DO NOT include any text or formatting outside of the JSON array.**

    ---
    ANALYSIS:
    {analysis}
    ---

    JSON_OUTPUT:
    """

    prompt = ChatPromptTemplate.from_template(generation_template)
    llm = get_llm()
    
    generation_chain = prompt | llm | StrOutputParser()

    try:
        response_str = generation_chain.invoke({"analysis": analysis, "url": url})
        
        # Clean the response to ensure it's valid JSON
        # The model sometimes wraps the JSON in ```json ... ```
        if "```json" in response_str:
            response_str = response_str.split("```json")[1].split("```")[0].strip()

        posts = json.loads(response_str)
        
        # Validate and format dates
        start_date = datetime.now().date() + timedelta(days=1)
        for i, post in enumerate(posts):
            # Simple scheduling logic: spread posts over 7 days
            day_offset = i % 7
            post['scheduled_date'] = (start_date + timedelta(days=day_offset)).strftime('%Y-%m-%d')
            post['approved'] = True # Default to approved for the UI

        logging.info(f"Successfully generated {len(posts)} social media posts.")
        return posts
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON from LLM response: {e}")
        logging.error(f"LLM Response was: {response_str}")
        return []
    except Exception as e:
        logging.error(f"An error occurred during content generation: {e}")
        return []
