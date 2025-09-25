Autonomous Social Media Campaign Agent
This project is a complete end-to-end system that takes a URL to a product announcement or blog post and generates a scheduled 7-day social media campaign for Twitter (X) and LinkedIn. It uses an AI agent to plan and execute the campaign, with a human-in-the-loop UI for approval.

Project Tree
/autonomous_campaign_agent
├── /agents
│   ├── __init__.py
│   └── content_generator.py
├── /nlp
│   ├── __init__.py
│   └── analysis.py
├── /scraper
│   ├── __init__.py
│   └── scraper.py
├── /scheduler
│   ├── __init__.py
│   └── scheduler.py
├── /ui
│   ├── __init__.py
│   └── app_ui.py
├── /tests
│   ├── __init__.py
│   ├── test_scraper.py
│   └── test_scheduler.py
├── app.py
├── requirements.txt
└── README.md

Features
Web Scraping: Scrapes the full text content from a given URL.
NLP Analysis: Uses an LLM (via LangChain and OpenAI) to extract key themes, statistics, and value propositions.
AI Content Generation: Drafts 5-7 tailored posts each for Twitter and LinkedIn based on the analysis.
Human-in-the-Loop UI: A Streamlit interface to review, edit, approve, or reject generated posts.
Mock Scheduling: Schedules approved posts in a local SQLite database, simulating a real-world scheduler.
Technical Stack
Python: 3.10+
Orchestration: LangChain
UI: Streamlit
LLM: OpenAI (GPT-3.5-Turbo or newer)
Scraping: requests & beautifulsoup4
Database: SQLite3 (for mock scheduling)

Setup and Installation

1. Clone the Repository
git clone <your-repo-url>
cd autonomous_campaign_agent


2. Create a Virtual Environment
It's highly recommended to use a virtual environment.
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`


3. Install Dependencies
pip install -r requirements.txt


4. Set Up Environment Variables
The application requires an OpenAI API key to function. Create a .env file in the root of the project directory:
OPENAI_API_KEY="your-openai-api-key-here"



