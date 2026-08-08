import os
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from src.agentic_rag.search import build_index, build_chunk_index
from src.agentic_rag.rag import RAGBase
from src.agentic_rag.data_loader import load_documents


# =========================================================
# Configuration
# =========================================================

load_dotenv()

QUERY_Q3 = "How does the agentic loop keep calling the model until it stops?"
QUERY_Q6 = "How does the agentic loop work, and how is it different from plain RAG?"

MODEL = "llama-3.3-70b-versatile"


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Agentic RAG Homework",
    page_icon="🤖",
    layout="wide",
)


# =========================================================
# Styling
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #777;
        margin-bottom: 30px;
    }

    .result-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        margin-bottom: 15px;
    }

    .answer {
        font-size: 28px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Header
# =========================================================

st.markdown(
    '<div class="main-title">🤖 Agentic RAG Homework</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "LLM ZoomCamp — Retrieval-Augmented Generation → Agentic RAG"
    "</div>",
    unsafe_allow_html=True,
)


# =========================================================
# API Client
# =========================================================

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error(
        "GROQ_API_KEY was not found in your .env file."
    )
    st.stop()

client = Groq(api_key=api_key)


# =========================================================
# Cached Data
# =========================================================

@st.cache_data
def get_documents():
    return load_documents()


@st.cache_resource
def get_normal_index():
    return build_index()


@st.cache_resource
def get_chunk_index():
    return build_chunk_index()


# =========================================================
# Homework Calculations
# =========================================================

def get_q1():
    documents = get_documents()
    return len(documents)


def get_q2():
    index = get_normal_index()

    results = index.search(
        "How does the agentic loop keep calling the model until it stops?",
        num_results=1,
    )

    if not results:
        return "No result found."

    return results[0]["filename"]


def get_q3():
    index = get_normal_index()

    rag = RAGBase(
        index=index,
        llm_client=client,
        model=MODEL,
    )

    answer, usage = rag.rag(QUERY_Q3)

    return {
        "answer": answer,
        "input_tokens": usage.prompt_tokens,
    }


def get_q4():
    index = get_chunk_index()

    # build_chunk_index internally loads all chunks.
    # We use the index documents to count them.
    return len(index.docs)


def get_q5():
    index = get_chunk_index()

    rag = RAGBase(
        index=index,
        llm_client=client,
        model=MODEL,
    )

    answer, usage = rag.rag(QUERY_Q3)

    return {
        "answer": answer,
        "input_tokens": usage.prompt_tokens,
    }


# =========================================================
# Main Dashboard
# =========================================================

st.header("📚 Homework Results")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Q1")
    st.caption("Number of lesson pages")

    if st.button("Run Q1", use_container_width=True):
        with st.spinner("Loading lesson pages..."):
            q1_result = get_q1()

        st.success(f"{q1_result} lesson pages")

with col2:
    st.subheader("Q2")
    st.caption("First search result")

    if st.button("Run Q2", use_container_width=True):
        with st.spinner("Searching index..."):
            q2_result = get_q2()

        st.success(q2_result)

with col3:
    st.subheader("Q4")
    st.caption("Number of chunks")

    if st.button("Run Q4", use_container_width=True):
        with st.spinner("Building chunk index..."):
            q4_result = get_q4()

        st.success(f"{q4_result} chunks")


st.divider()


# =========================================================
# Q3
# =========================================================

st.header("🧠 Q3 — RAG")

st.write(
    "How does the agentic loop keep calling the model until it stops?"
)

if st.button("Run Q3", use_container_width=True):

    with st.spinner("Running RAG..."):

        q3_result = get_q3()

    st.subheader("Input Tokens")

    st.metric(
        "Prompt Tokens",
        q3_result["input_tokens"],
    )

    st.subheader("Answer")

    st.write(q3_result["answer"])


st.divider()


# =========================================================
# Q5
# =========================================================

st.header("✂️ Q5 — RAG with Chunking")

st.write(
    "The same RAG question using the chunked index."
)

if st.button("Run Q5", use_container_width=True):

    with st.spinner("Running chunked RAG..."):

        q5_result = get_q5()

    st.subheader("Input Tokens")

    st.metric(
        "Prompt Tokens",
        q5_result["input_tokens"],
    )

    st.subheader("Answer")

    st.write(q5_result["answer"])


st.divider()


# =========================================================
# Q6 — Agentic RAG
# =========================================================

st.header("🤖 Q6 — Agentic RAG")

st.write(
    "Ask the Agentic RAG system a question about the course."
)

user_query = st.text_area(
    "Your question",
    value=QUERY_Q6,
    height=100,
)


if st.button(
    "🚀 Ask Agent",
    type="primary",
    use_container_width=True,
):

    from openai import OpenAI

    from toyaikit.llm import OpenAIClient
    from toyaikit.tools import Tools
    from toyaikit.chat.runners import (
        OpenAIResponsesRunner,
        RunnerCallback,
    )

    # -----------------------------------------------------
    # Groq OpenAI-compatible client
    # -----------------------------------------------------

    groq_client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )

    # -----------------------------------------------------
    # Chunk index
    # -----------------------------------------------------

    index = get_chunk_index()

    # -----------------------------------------------------
    # Search tool
    # -----------------------------------------------------

    def search(query: str) -> list[dict]:
        """
        Search the course lessons for relevant information.
        """

        return index.search(
            query,
            num_results=3,
        )

    # -----------------------------------------------------
    # Tool registration
    # -----------------------------------------------------

    agent_tools = Tools()

    agent_tools.add_tool(search)

    # -----------------------------------------------------
    # LLM
    # -----------------------------------------------------

    llm_client = OpenAIClient(
        model="openai/gpt-oss-20b",
        client=groq_client,
    )

    # -----------------------------------------------------
    # Instructions
    # -----------------------------------------------------

    instructions = """
    You're a course teaching assistant.
    Answer the student's question using the search tool.
    Make multiple searches with different keywords before answering.
    """

    # -----------------------------------------------------
    # Callback
    # -----------------------------------------------------

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

    callback = SearchCallCounter()

    # -----------------------------------------------------
    # Runner
    # -----------------------------------------------------

    runner = OpenAIResponsesRunner(
        tools=agent_tools,
        developer_prompt=instructions,
        llm_client=llm_client,
    )

    # -----------------------------------------------------
    # Run Agent
    # -----------------------------------------------------

    with st.spinner("Agent is searching and reasoning..."):

        result = runner.loop(
            prompt=user_query,
            callback=callback,
        )

    # -----------------------------------------------------
    # Display result
    # -----------------------------------------------------

    st.subheader("Agent Answer")

    st.write(result.last_message)

    st.subheader("Agent Statistics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Search Calls",
            callback.count,
        )

    with col2:
        st.metric(
            "Input Tokens",
            result.tokens.input_tokens,
        )


st.divider()


# =========================================================
# Footer
# =========================================================

st.caption(
    "Built as part of the DataTalksClub LLM ZoomCamp — Agentic RAG Homework."
)