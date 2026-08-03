from __future__ import annotations

import os
from typing import TypedDict, List

from dotenv import load_dotenv
from openai import OpenAI

from langgraph.graph import StateGraph, END
from langchain_community.document_loaders import DirectoryLoader, TextLoader

from faq import FAQS
from rag import search_knowledge

# ---------------------------------------------------
# Environment Configuration
# ---------------------------------------------------

load_dotenv()

OLLAMA_API_KEY = os.getenv("OLLAMAAPIKEY")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:cloud")

if not OLLAMA_API_KEY:
    raise ValueError("OLLAMAAPIKEY not found in .env")

client = OpenAI(
    api_key=OLLAMA_API_KEY,
    base_url="https://ollama.com/v1"
)

# ---------------------------------------------------
# Load Knowledge Base
# ---------------------------------------------------

try:
    loader = DirectoryLoader(
        "knowledge",
        glob="*.txt",
        loader_cls=TextLoader
    )

    docs = loader.load()

    KNOWLEDGE = "\n\n".join(
        doc.page_content for doc in docs
    )

    print(f"Knowledge files loaded: {len(docs)}")

except Exception as error:

    KNOWLEDGE = ""

    print(f"Knowledge loading failed: {error}")

# ---------------------------------------------------
# Agent State
# ---------------------------------------------------

class AgentState(TypedDict):
    message: str
    response: str
    history: List[dict]
    is_related: bool
    is_faq: bool


# ---------------------------------------------------
# Technical Topics
# ---------------------------------------------------

TECH_TOPICS = {
    "python",
    "fastapi",
    "langchain",
    "langgraph",
    "github",
    "render",
    "ollama",
    "ai",
    "machine learning",
    "deep learning",
    "project",
    "assignment",
    "deployment",
    "docker",
    "api",
    "html",
    "css",
    "javascript",
    "sql",
    "internship",
    "devforge",
}

# ---------------------------------------------------
# Helper Functions
# ---------------------------------------------------

def is_technical_question(question: str) -> bool:
    """
    Returns True if the question is related to
    DEVFORGE or technical topics.
    """

    question = question.lower()

    score = 0

    for topic in TECH_TOPICS:
        if topic in question:
            score += 1

    return score >= 1


def get_faq_answer(question: str):

    question = question.lower()

    for faq_question, faq_answer in FAQS.items():

        if faq_question in question:
            return faq_answer

    return None