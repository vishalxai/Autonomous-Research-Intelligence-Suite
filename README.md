# 🚀 Autonomous Research Intelligence Suite

An advanced, hybrid Multi-Agent AI system built with AutoGen. This suite demonstrates enterprise-grade architecture by seamlessly orchestrating local edge models (Ollama) and cloud-based LLMs (OpenRouter) to perform deep multimodal research, extract structured data, and dynamically route around API congestion.

## 🏗️ Architectural Highlights

Building reliable AI systems requires more than just API calls. This project implements resilient, self-healing patterns:

* **Hybrid Brain Orchestration:** Combines the zero-latency privacy of local edge models (Llama 3.2 via Ollama) with the massive reasoning scale of cloud models (Llama 3.3 70B, Google Gemma 3).
* **Self-Healing State Management:** Utilizes AutoGen's `RoundRobinGroupChat` to natively handle memory sync between isolated agents. Integrates an auto-routing load balancer to dynamically bypass `429 Rate Limit` and `404 Not Found` errors during high server traffic.
* **Resilient Structured Output:** Bypasses the common "JSON hallucination" issue found in smaller local models by using Literal Prompt Templating alongside strict Pydantic validation.
* **Multimodal Vision Routing:** Equips agents with "eyes" by routing image payloads to specialized visual-language models (e.g., Nvidia Nemotron Nano 12B VL) for environmental and agricultural analysis.

## 💻 Tech Stack

* **Framework:** [AutoGen (v0.4)](https://microsoft.github.io/autogen/)
* **Local Inference:** [Ollama](https://ollama.com/) (Llama 3.2)
* **Cloud API Gateway:** [OpenRouter](https://openrouter.ai/) 
* **Data Validation:** [Pydantic](https://docs.pydantic.dev/)

## 🤖 Agent Personas in Action

1. **The Cloud Researcher:** A heavy-weight cloud model tasked with deep-dive analysis and multimodal landscape inspection.
2. **The Local Formatter:** A local edge model that securely ingests the researcher's output and formats it into strict, pipeline-ready JSON and bullet points. 

## ⚙️ Quick Start

**1. Clone the repository**
```bash
git clone [https://github.com/vishalxai/Autonomous-Research-Intelligence-Suite.git](https://github.com/vishalxai/Autonomous-Research-Intelligence-Suite.git)
cd Autonomous-Research-Intelligence-Suite
```

**2. Set up your environment**
Ensure you have Python 3.10+ installed.
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Configure Environment Variables**
Create a `.env` file in the root directory and add your OpenRouter API key:
```env
OPENROUTER_API_KEY=your_api_key_here
```

**4. Start the Local Brain**
Ensure you have Ollama installed and running on your machine:
```bash
ollama run llama3.2
```

**5. Run the Multi-Agent Team**
Execute the Jupyter Notebooks to watch the autonomous baton pass in real-time.

---
*Built with grit, local hardware, and the AutoGen framework.*
```

