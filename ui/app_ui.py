# ui/app_ui.py
import streamlit as st
import pandas as pd
from scraper.scraper import scrape_text_from_url
from nlp.analysis import analyze_text
from agents.content_generator import generate_campaign_content
from scheduler.scheduler import MockScheduler

def initialize_session_state():
    """Initializes session state variables."""
    if 'campaign_generated' not in st.session_state:
        st.session_state.campaign_generated = False
    if 'campaign_posts' not in st.session_state:
        st.session_state.campaign_posts = []
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = ""

def run_agent_workflow(url):
    """Orchestrates the agent workflow from scraping to content generation."""
    with st.spinner("Step 1: Scraping website content..."):
        scraped_text = scrape_text_from_url(url)
        if not scraped_text:
            st.error("Failed to scrape the URL. Please check the URL and try again.")
            return

    with st.spinner("Step 2: Analyzing content with AI..."):
        analysis = analyze_text(scraped_text)
        if not analysis or "Error" in analysis:
            st.error("Failed to analyze the content.")
            return
        st.session_state.analysis_result = analysis
        st.session_state.analysis_complete = True

    with st.spinner("Step 3: Generating social media campaign..."):
        posts = generate_campaign_content(analysis, url)
        if not posts:
            st.error("Failed to generate the campaign content.")
            return
        st.session_state.campaign_posts = posts
        st.session_state.campaign_generated = True

def main():
    """Main function to run the Streamlit UI."""
    st.set_page_config(page_title="Autonomous Social Media Agent", layout="wide")
    
    st.title("🚀 Autonomous Social Media Campaign Agent")
    st.markdown("Enter a URL of a product announcement or blog post to automatically generate a 7-day social media campaign.")

    initialize_session_state()

    # --- 1. URL Input ---
    url = st.text_input("Enter URL here:", "[https://langchain.ai/blog/langchain-v0-2-and-langsmith-v0-1-in-beta](https://langchain.ai/blog/langchain-v0-2-and-langsmith-v0-1-in-beta)", key="url_input")

    if st.button("Generate Campaign", type="primary"):
        if url:
            # Reset state for a new run
            st.session_state.campaign_generated = False
            st.session_state.campaign_posts = []
            st.session_state.analysis_complete = False
            st.session_state.analysis_result = ""
            run_agent_workflow(url)
        else:
            st.warning("Please enter a URL.")

    # --- 2. Display Analysis and Campaign for Approval ---
    if st.session_state.analysis_complete:
        with st.expander("📝 View AI Analysis", expanded=False):
            st.markdown(st.session_state.analysis_result)

    if st.session_state.campaign_generated:
        st.header("✍️ Review and Approve Your Campaign")
        st.markdown("You can edit the content, change dates, or remove posts before scheduling.")

        df = pd.DataFrame(st.session_state.campaign_posts)
        
        # Ensure correct column order and data types
        df['scheduled_date'] = pd.to_datetime(df['scheduled_date'])
        df = df[['approved', 'platform', 'scheduled_date', 'content']]

        # Use st.data_editor for an editable table
        edited_df = st.data_editor(
            df,
            column_config={
                "approved": st.column_config.CheckboxColumn(
                    "Approve?",
                    default=True,
                ),
                "platform": st.column_config.TextColumn("Platform", disabled=True),
                "scheduled_date": st.column_config.DateColumn(
                    "Schedule Date",
                    format="YYYY-MM-DD",
                ),
                "content": st.column_config.TextColumn("Post Content", width="large")
            },
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic"
        )

        if st.button("Approve and Schedule Campaign", type="primary"):
            approved_posts = edited_df[edited_df['approved']].to_dict('records')
            
            if not approved_posts:
                st.warning("No posts were approved for scheduling.")
            else:
                with MockScheduler() as scheduler:
                    scheduler.initialize_db()
                    with st.spinner("Scheduling approved posts..."):
                        for post in approved_posts:
                            scheduler.schedule_post(
                                platform=post['platform'],
                                content=post['content'],
                                scheduled_date=post['scheduled_date'].strftime('%Y-%m-%d')
                            )
                st.success(f"✅ Successfully scheduled {len(approved_posts)} posts!")
                st.session_state.campaign_scheduled = True


    # --- 3. Display Scheduled Posts ---
    st.header("🗓️ Scheduled Posts")
    with MockScheduler() as scheduler:
        scheduler.initialize_db() # Ensure table exists
        scheduled_posts = scheduler.get_all_scheduled_posts()
        if scheduled_posts:
            scheduled_df = pd.DataFrame(scheduled_posts)
            st.dataframe(scheduled_df, use_container_width=True, hide_index=True)
        else:
            st.info("No posts are currently scheduled.")

if __name__ == '__main__':
    main()

