Agentic RAG Homework — LLM ZoomCamp

An implementation of the Agentic RAG homework from the DataTalks.Club LLM ZoomCamp.

The project starts with basic retrieval and RAG, adds document chunking, and then turns the search capability into a tool that an LLM can call inside an agentic loop.

A Streamlit UI is included to run and display the results of Q1–Q6.

Project Overview :

This project covers the progression:

Course Lessons
     │
     ▼
Document Loading
     │
     ▼
Search / Retrieval
     │
     ▼
Plain RAG
     │
     ▼
Document Chunking
     │
     ▼
RAG with Chunking
     │
     ▼
Search Tool
     │
     ▼
Agentic RAG
     │
     ▼
Streamlit UI

The main goal is to understand the difference between a fixed RAG pipeline and an agentic workflow where the LLM can decide when to call a search tool and continue iterating until it can produce an answer.

Technologies Used :

Python 3.11+

uv for Python environment and dependency management

Groq API

OpenAI-compatible API client

ToyAIKit

MinSearch

GitSource

Streamlit

python-dotenv

Requirements :

You need:

Python 3.11 or newer

uv

A Groq API key

The project uses the Groq OpenAI-compatible endpoint for the agentic workflow.

Environment Setup

Clone the repository and enter the project directory.

Install dependencies with:

uv sync

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key

The API key is loaded with python-dotenv.

Important: .env is excluded from Git with .gitignore. Never commit the API key.

Project Structure :

LLM_ZoomCamp_Agentic-RAG_Homework/
│
├── q1.py
├── q2.py
├── q3.py
├── q4.py
├── q5.py
├── q6.py
│
├── src/
│   └── agentic_rag/
│       ├── __init__.py
│       ├── data_loader.py
│       ├── search.py
│       ├── chunking.py
│       └── rag.py
│
├── ui/
│   └── app.py
│
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
└── README.md

Main modules :

data_loader.py :

Loads Markdown lesson files from the DataTalksClub/llm-zoomcamp repository using a fixed commit and prepares them as documents.

search.py :

Builds MinSearch indexes for:

the original lesson documents

the chunked lesson documents

chunking.py :

Splits lesson documents into overlapping chunks using gitsource.chunk_documents.

Current configuration:

size=2000
step=1000

rag.py :

Contains the reusable RAG implementation:

Search the index

Build the retrieved context

Build the prompt

Send the prompt to the LLM

Return the generated answer and token usage

q1.py → q6.py : 

Contain the individual homework tasks and experiments.

ui/app.py :

Provides the Streamlit interface for running and displaying Q1–Q6 and the Agentic RAG workflow.

Homework Results :

Q1 — Total Lesson Pages

The lesson repository contains:

72 lesson pages

Result: 72

Q2 — Search Query

The search query is used to find information about the agentic loop.

The first relevant search result was:

01-agentic-rag/lessons/14-agentic-loop.md

Result:

01-agentic-rag/lessons/14-agentic-loop.md

Q3 — RAG

Q3 demonstrates the basic RAG flow.

The implementation follows:

User Question
      │
      ▼
Search Index
      │
      ▼
Retrieved Documents
      │
      ▼
Build Context
      │
      ▼
Prompt + Context
      │
      ▼
LLM
      │
      ▼
Answer

The important idea is that the LLM does not search the course itself. The application performs retrieval first and then provides the retrieved information as context to the model.

The tested implementation produced an answer explaining the agentic loop and its while True control flow.

So The total input (prompt) tokens did we send to the model for this request is 5799.

Q4 — Chunking

The lesson documents are split into overlapping chunks.

Current configuration:

Chunk size: 2000
Step:       1000

The resulting chunk index contains:

295 chunks

Result: 295 chunks

Chunking allows retrieval to operate on smaller pieces of documents instead of always retrieving an entire lesson.

Q5 — RAG with Chunking

Q5 uses the chunked index instead of the original document index.

The flow becomes:

Question
   │
   ▼
Chunked Search Index
   │
   ▼
Relevant Chunks
   │
   ▼
Context
   │
   ▼
LLM
   │
   ▼
Answer

The tested implementation successfully answered the agentic-loop question using the chunked index.

The recorded prompt/input token count for the tested run was approximately:

1526

Q6 — Agentic RAG

Q6 changes the architecture from a fixed RAG pipeline into an agentic workflow.

Instead of always doing:

Search → Build Context → LLM → Answer

the LLM receives a search tool and can decide when to use it.

The workflow is conceptually:

                 ┌──────────────────────┐
                 │        User          │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │         LLM          │
                 └──────────┬───────────┘
                            │
                   Tool call required?
                     ┌──────┴──────┐
                    Yes            No
                     │              │
                     ▼              ▼
              ┌────────────┐   ┌───────────┐
              │   Search   │   │   Final   │
              │    Tool    │   │  Answer   │
              └─────┬──────┘   └───────────┘
                    │
                    ▼
              Tool result
                    │
                    ▼
                  LLM
                    │
                    └─────── loop ────────►

The agent can make multiple searches with different queries before producing its final answer.

Search Tool

The search function is registered with ToyAIKit as a tool.

It uses a typed parameter and a docstring so ToyAIKit can generate the tool schema automatically.

Conceptually:

def search(query: str) -> list[dict]:
    """
    Search the course lessons for relevant information.
    """
    return index.search(
        query,
        num_results=3,
    )

The important difference is that the search operation is now available to the model as an action rather than being hard-coded as one fixed step.

Agentic Loop

The agentic loop follows this pattern:

1. Send the current conversation and available tools to the LLM.
2. Check whether the LLM requested a tool call.
3. If it requested search, execute the search.
4. Add the search result back to the conversation.
5. Call the LLM again with the updated context.
6. Repeat until the LLM returns a response without another tool call.
7. Return the final answer.

This is the same core idea as the handwritten while True loop from the Agentic RAG lesson.

ToyAIKit handles the repetitive function-call and message-management logic.

Agentic RAG vs Plain RAG

Feature

Plain RAG

Agentic RAG

Control flow

Fixed

Dynamic

Retrieval

Application performs retrieval

LLM can decide to call search

Tool calls

Usually one fixed retrieval step

Can make multiple tool calls

Iteration

Normally single-pass

Iterative

Decision making

Hard-coded pipeline

LLM-driven

Best for

Simple question answering

Multi-step or adaptive tasks

In short:

Plain RAG is a fixed retrieve-then-generate pipeline, while Agentic RAG allows the LLM to control the retrieval process through tools and an iterative loop.

Q6 Tested Result

The final Agentic RAG UI successfully answered:

How does the agentic loop work, and how is it different from plain RAG?

The tested run demonstrated multiple search calls before the final response.

Example recorded statistics:

Search calls: 4
Input tokens: 16663

Token usage can vary between runs because the agent may perform a different number of model/tool iterations.

Streamlit UI

The project includes a Streamlit interface for demonstrating the homework.

Run it with:

uv run streamlit run ui/app.py

Then open:

http://localhost:8501

The UI provides sections for:

Q1 — Lesson pages

Q2 — Search result

Q3 — RAG

Q4 — Chunk count

Q5 — RAG with chunking

Q6 — Agentic RAG

The Q6 section also displays the agent answer and useful execution statistics such as search calls and token usage.

Running the Homework from the Terminal

Individual questions can be executed with:

uv run python q1.py
uv run python q2.py
uv run python q3.py
uv run python q4.py
uv run python q5.py
uv run python q6.py

To launch the complete UI:

uv run streamlit run ui/app.py

Dependencies

Dependencies are managed through pyproject.toml and locked in uv.lock.

To reproduce the environment:

uv sync

This installs the project dependencies into the local virtual environment.

Security

The Groq API key is stored in:

.env

The .env file is ignored by Git:

.env

The virtual environment is also ignored:

.venv

No API credentials should be committed to the repository.

Learning Outcomes

By completing this homework, the project demonstrates understanding of:

Retrieval-Augmented Generation (RAG)

Search and retrieval

Document indexing

Document chunking

Context construction

LLM prompting

Tool calling

Agentic workflows

Agent loops

Iterative search

Token usage tracking

Building a simple Agentic RAG application

Exposing the system through a Streamlit UI

The progression is:

RAG
  ↓
Better retrieval
  ↓
Chunking
  ↓
RAG with chunks
  ↓
Search as a tool
  ↓
Agentic loop
  ↓
Agentic RAG application

Notes

The project uses a fixed commit of the course repository for reproducible lesson loading.

Agentic RAG responses and token counts may vary between runs.

ToyAIKit is used as a small teaching/experimentation library for the agent loop.

The project is intended as an educational implementation of the LLM ZoomCamp homework, not as a production Agentic RAG system.

Author

Andrew Sameh

LLM ZoomCamp — Agentic RAG Homework

Built as part of the DataTalks.Club LLM ZoomCamp.