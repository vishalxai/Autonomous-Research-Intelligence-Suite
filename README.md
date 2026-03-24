# 🚀 Autonomous Research Intelligence Suite

An advanced, hybrid Multi-Agent AI system built with AutoGen. This suite demonstrates enterprise-grade architecture by seamlessly orchestrating local edge models (Ollama) and cloud-based LLMs (OpenRouter) to perform deep multimodal research, extract structured data, dynamically route around API congestion, and present findings via a deployed web interface.

## 🏗️ Architectural Highlights

Building reliable AI systems requires more than just API calls. This project implements resilient, self-healing patterns and full-stack deployment:

* **Custom Tool Execution:** Extends agent capabilities using AutoGen's `FunctionTool` to securely connect to external databases (ArXiv API), retrieve raw JSON payloads, and pass them into the agentic workflow.
* **Decoupled Architecture (Frontend/Backend):** Separates the heavy multi-agent reasoning logic (`backend.py`) from the user interface (`app.py`), enabling seamless deployment to Streamlit Community Cloud.
* **Hybrid Brain Orchestration:** Combines the zero-latency privacy of local edge models (Llama 3.2 via Ollama) with the massive reasoning scale of cloud models (Llama 3.3 70B, Google Gemma 3).
* **Self-Healing State Management:** Utilizes AutoGen's `RoundRobinGroupChat` to natively handle memory sync between isolated agents and dynamically bypass `429 Rate Limit` and `404 Not Found` errors.
* **Resilient Structured Output:** Bypasses "JSON hallucination" found in smaller local models by using strict Prompt Engineering and literal templating alongside Pydantic validation.

## 💻 Tech Stack

* **Framework:** [AutoGen (v0.4+)](https://microsoft.github.io/autogen/)
* **Frontend UI:** [Streamlit](https://streamlit.io/)
* **External APIs:** [ArXiv](https://pypi.org/project/arxiv/) 
* **Cloud API Gateway:** [OpenRouter](https://openrouter.ai/) 
* **Local Inference:** [Ollama](https://ollama.com/) (Llama 3.2)

## 🤖 Agent Personas in Action

This suite utilizes specific agent personas divided across different tasks:

1. **The Search Agent (ArXiv Module):** Equipped with custom Python functions to securely query the ArXiv database and retrieve real-time, factual academic papers.
2. **The Summarizer Agent (ArXiv Module):** A strict editorial agent that ingests raw JSON academic data and formats it into clean, hallucination-free Markdown with clickable PDF links.
3. **The Cloud Researcher (Core Module):** A heavy-weight cloud model tasked with deep-dive analysis and multimodal landscape inspection.
4. **The Local Formatter (Core Module):** A local edge model that securely ingests the researcher's output and formats it into strict, pipeline-ready JSON. 

## ⚙️ Quick Start

**1. Clone the repository**
```bash
git clone [https://github.com/vishalxai/Autonomous-Research-Intelligence-Suite.git](https://github.com/vishalxai/Autonomous-Research-Intelligence-Suite.git)
cd Autonomous-Research-Intelligence-Suite

2. Set up your environment
Ensure you have Python 3.10+ installed.
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Configure Environment Variables
Create a .env file in the root directory and add your OpenRouter API key:
OPENROUTER_API_KEY=your_api_key_here


4. Launch the ArXiv Web Application
Spin up the Streamlit interface to test the Multi-Agent Literature Reviewer:
streamlit run Autogen_Arxiv_research_Project/app.py

5. Start the Local Brain (Optional - for local agent testing)
Ensure you have Ollama installed and running on your machine:

ollama run llama3.2
