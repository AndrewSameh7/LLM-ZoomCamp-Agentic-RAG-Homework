import os

from dotenv import load_dotenv
from openai import OpenAI

from toyaikit.llm import OpenAIClient
from toyaikit.tools import Tools
from toyaikit.chat.runners import (
    OpenAIResponsesRunner,
    RunnerCallback,
)

from src.agentic_rag.search import build_chunk_index


load_dotenv()


QUERY = "How does the agentic loop work, and how is it different from plain RAG?"

INSTRUCTIONS = """
You're a course teaching assistant. Answer the student's question using the search tool.
Make multiple searches with different keywords before answering.
"""


class SearchCallCounter(RunnerCallback):
    def __init__(self):
        self.count = 0

    def on_function_call(self, function_call, result):
        if function_call.name == "search":
            self.count += 1

    def on_message(self, message):
        pass

    def on_reasoning(self, reasoning):
        pass

    def on_response(self, response):
        pass


def main():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY was not found in .env")

    groq_client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )

    index = build_chunk_index()

    def search(query: str) -> list[dict]:
        """
        Search the course lessons for relevant information.
        """
        return index.search(
            query,
            num_results=3,
        )

    agent_tools = Tools()
    agent_tools.add_tool(search)

    llm_client = OpenAIClient(
        model="openai/gpt-oss-20b",
        client=groq_client,
    )

    runner = OpenAIResponsesRunner(
        tools=agent_tools,
        developer_prompt=INSTRUCTIONS,
        llm_client=llm_client,
    )

    callback = SearchCallCounter()

    result = runner.loop(
        prompt=QUERY,
        callback=callback,
    )

    print("Q6 - Query:")
    print(QUERY)

    print("\nAnswer:")
    print(result.last_message)

    print("\nInput tokens:")
    print(result.tokens.input_tokens)

    print("\nSearch calls:")
    print(callback.count)


if __name__ == "__main__":
    main()