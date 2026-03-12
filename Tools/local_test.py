import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool

# 1. Initialize the Local Model via Ollama using Llama 3.2
openai_client = OpenAIChatCompletionClient(
    model="llama3.2",
    api_key="placeholder",
    base_url="http://localhost:11434/v1",
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": "llama3",
        "structured_output": True  # Llama 3.2 handles structured output well
    },
)

# 2. Define the tool
def reverse_string(text: str) -> str:
    """Reverse the given text."""
    return text[::-1]

reverse_tool = FunctionTool(reverse_string, description='A tool to reverse a string')

# 3. Create the specialized agent
agent = AssistantAgent(
    name="ReverseAgent",
    model_client=openai_client,
    system_message="You are a helpful assistant. Use the reverse_string tool to help the user.",
    tools=[reverse_tool],
    reflect_on_tool_use=True,
)

# 4. Execution logic
async def main():
    task = "Reverse the text 'Hello, how are you Doing?'"
    result = await agent.run(task=task)
    print(f"Agent Response: {result.messages[-1].content}")

if __name__ == "__main__":
    asyncio.run(main())