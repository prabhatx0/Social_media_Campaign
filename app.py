# app.py
import os
from dotenv import load_dotenv
from ui.app_ui import main

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if the OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please create a .env file and add your OpenAI API key.")
    else:
        main()
