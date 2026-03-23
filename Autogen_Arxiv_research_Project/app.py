import streamlit as st
import asyncio

# Import the orchestrator function from our backend file
from backend import run_literature_review

# Configure the Streamlit Page
st.set_page_config(page_title="ArXiv AI Researcher", page_icon="📚", layout="centered")

st.title("📚 Autonomous ArXiv Researcher")
st.markdown("Enter a topic, and my multi-agent AI team will fetch, read, and summarize the latest research for you.")

# User Inputs
topic = st.text_input("Research Topic:", placeholder="e.g., Quantum Machine Learning")
max_papers = st.slider("Number of papers to review:", min_value=1, max_value=5, value=3)

# Search Button
if st.button("Start Research"):
    if not topic:
        st.warning("Please enter a research topic first.")
    else:
        # Create visual containers for the output
        status_text = st.empty()
        agent_logs = st.empty()
        final_summary = st.empty()
        
        status_text.info("🚀 Booting up AI Agents...")
        
        # We need a wrapper to run the async backend code inside Streamlit
        async def run_ui():
            log_output = ""
            
            # Stream the agent thoughts
            async for message in run_literature_review(topic=topic, max_results=max_papers):
                sender = getattr(message, 'source', 'System')
                
                # We only want to print text messages, not raw tool executions
                if hasattr(message, 'content') and isinstance(message.content, str):
                    if sender == "Search_Agent":
                        status_text.info("🔍 Search Agent is querying ArXiv and fetching data...")
                        log_output += f"**{sender}:** Found papers. Passing to Summarizer...\n\n"
                        agent_logs.markdown(log_output)
                        
                    elif sender == "Summarizer_Agent":
                        status_text.success("✨ Summarizer Agent has formatted the final report!")
                        # Print the final beautiful markdown in its own container
                        final_summary.markdown(f"### Final Report\n{message.content}")

        # Execute the async function
        asyncio.run(run_ui())