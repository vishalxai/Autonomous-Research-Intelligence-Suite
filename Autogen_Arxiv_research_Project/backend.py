import asyncio 
import arxiv
from typing import List,Dict,Any
import os 
from dotenv import load_dotenv

#AutoGen Imports 
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.tools import FunctionTool 
from autogen_ext.models.openai import OpenAIChatCompletionClient

#Load Environemnt Variables
load_dotenv()

# 1. Define the Custom Tool (Connecting to Arxiv)
def search_arxiv(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """ Searches Arxiv for research papers and returns their details."""
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    results = []
    for paper in client.results(search):
        results.append({
            "title": paper.title,
            "authors": [author.name for author in paper.authors],
            "published": paper.published.strftime("%Y-%m-%d"),
            "summary": paper.summary,
            "pdf_url": paper.pdf_url    
        })
    return results

# Wrap the python function into an AutoGen Tool
arxiv_tool = FunctionTool(search_arxiv, description="Searches Arxiv for research papers based on a query.")

# 2.Build the Multi-Agent Team (One Agent to Search, One Agent to Summarize)
def build_team():
   # Setup the Model Client (Using the Llama 3.3 model you proved earlier via OpenRouter)
    model_client = OpenAIChatCompletionClient(
        model="meta-llama/llama-3.3-70b-instruct",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "unknown"
        }
    )
    # Agent 1: The Researcher
    search_agent = AssistantAgent(
        name="Search_Agent",
        model_client=model_client,
        tools=[arxiv_tool],
        reflect_on_tool_use=True,
        system_message=(
            "You are a Research Assistant. Given a topic, use the 'search_arxiv' tool "
            "to fetch relevant academic papers. You MUST return the EXACT raw data to the summarizer, "
            "including the exact 'pdf_url' for every single paper. Do not summarize the links away."
        )
    )

    # Agent 2: The Summarizer
    summarizer_agent = AssistantAgent(
        name="Summarizer_Agent",
        model_client=model_client,
        system_message=(
            "You are a Senior Academic Editor. Your job is to take the raw paper data "
            "provided by the Search Agent and format it into a beautiful Markdown summary. "
            "Include the Title, Authors, Published Date, and a brief 2-sentence summary. "
            "CRITICAL: You MUST include a clickable PDF link using ONLY the exact 'pdf_url' "
            "provided by the Search Agent. NEVER hallucinate, make up, or use example.com URLs."
        )
    )

    # Create a 2-turn round robin team(Search -> Summarize)
    team = RoundRobinGroupChat(
        participants=[search_agent, summarizer_agent],
        max_turns=2 
    )
    return team

# 3. The Orchestrator (Streams output to Streamlit)
async def run_literature_review(topic: str, max_results: int):
    team = build_team()
    
    # We embed the user's variables into the prompt
    task_prompt = f"Find {max_results} recent papers on the topic of: {topic}"
    
    # Stream the thought process
    async for message in team.run_stream(task=task_prompt):
        yield message



# --- TEST EXECUTION BLOCK ---
# This will only run if you execute this file directly in the terminal
if __name__ == "__main__":
    async def main():
        print("🚀 Starting the ArXiv Research Team...")
        print("-" * 50)
        
        # We will ask the team to find 2 papers on "Multi-Agent Systems"
        async for message in run_literature_review(topic="Multi-Agent Systems", max_results=2):
            
            # Extract the sender's name
            sender = getattr(message, 'source', 'System')
            print(f"\n🗣️ --- {sender} ---")
            
            # Print the content safely
            if hasattr(message, 'content'):
                print(message.content)
            else:
                print(message)
                
        print("\n✅ Backend Test Complete!")

    # Run the async loop
    asyncio.run(main())