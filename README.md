Autonomous Social Media Campaign AgentThis project is a complete end-to-end system that takes a URL to a product announcement or blog post and generates a scheduled 7-day social media campaign for Twitter (X) and LinkedIn. It uses an AI agent to plan and execute the campaign, with a human-in-the-loop UI for approval.Project Tree/autonomous_campaign_agent
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

FeaturesWeb Scraping: Scrapes the full text content from a given URL.NLP Analysis: Uses an LLM (via LangChain and OpenAI) to extract key themes, statistics, and value propositions.AI Content Generation: Drafts 5-7 tailored posts each for Twitter and LinkedIn based on the analysis.Human-in-the-Loop UI: A Streamlit interface to review, edit, approve, or reject generated posts.Mock Scheduling: Schedules approved posts in a local SQLite database, simulating a real-world scheduler.Technical StackPython: 3.10+Orchestration: LangChainUI: StreamlitLLM: OpenAI (GPT-3.5-Turbo or newer)Scraping: requests & beautifulsoup4Database: SQLite3 (for mock scheduling)Setup and Installation

1. Clone the Repositorygit clone <your-repo-url>
cd autonomous_campaign_agent
2. Create a Virtual EnvironmentIt's highly recommended to use a virtual environment.python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
3. Install Dependenciespip install -r requirements.txt
4. Set Up Environment VariablesThe application requires an OpenAI API key to function. Create a .env file in the root of the project directory:OPENAI_API_KEY="your-openai-api-key-here"
The application will load this key automatically.How to RunLaunch the Streamlit application with the following command:streamlit run app.py
Your web browser should open to the application's UI.Usage GuideEnter URL: Paste the URL of the blog post or product announcement you want to create a campaign for.Generate Campaign: Click the "Generate Campaign" button. The agent will begin the process of scraping, analyzing, and generating content. You can see the agent's progress in the status updates.Review & Approve: The generated posts for Twitter and LinkedIn will be displayed in editable tables. You can modify the text, change the scheduled date, or delete a post entirely.Schedule Campaign: Once you are satisfied with the posts, click the "Approve and Schedule Campaign" button. The posts will be saved to the mock scheduler database (campaign.db).View Scheduled Posts: A confirmation message will appear, and you can see the final scheduled posts in a table at the bottom of the page.Running TestsTo run the unit tests, use pytest:pytest
