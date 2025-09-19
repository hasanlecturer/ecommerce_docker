from litellm import completion
from dotenv import load_dotenv
import os
import re
import requests
import wikipedia
from pydantic import BaseModel


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Make sure LiteLLM sees the key
os.environ["GROQ_API_KEY"] = GROQ_API_KEY


def clean_think_tags(text):
    """Remove <think>...</think> tags and their content from the text."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


system_prompt = """
Context:
Your Name is SundorBot.
You are a Python assistant integrated into a Django backend. 
You answer Python-related questions and simple casual greetings.
You also have access to two tools:

Tools:
1. search_web(query): Searches the web using DuckDuckGo. Use it when you need general information outside Python.
2. search_wikipedia(query): Fetches a summary from Wikipedia. Use it for factual questions that can be answered from Wikipedia.

Rules:
- If you add in answer which tool you used.
- Only answer Python questions fully.
- You may answer casual greetings like "hi", "how are you", or "bye".
- If the question requires external information, automatically use the appropriate tool.
- If the question is neither Python nor casual nor requires tools, respond exactly:
  "I am sorry, I can only answer python related questions."
"""


def search_web(query: str) -> str:
    """Search DuckDuckGo for a query and return top result snippet"""
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}

    try:
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return f"Error during web search: {str(e)}"

    if data.get("AbstractText"):
        return data["AbstractText"]
    elif data.get("RelatedTopics"):
        for item in data["RelatedTopics"]:
            if "Text" in item:
                return item["Text"]
            elif "Topics" in item and len(item["Topics"]) > 0:
                return item["Topics"][0].get("Text", "No results found")
    return "No results found."


def search_wikipedia(query: str) -> str:
    """Fetch a summary from Wikipedia"""
    try:
        result = wikipedia.summary(query, sentences=3, auto_suggest=True, redirect=True)
        return result.replace("\n", " ")
    except wikipedia.DisambiguationError as e:
        return f"Your query is ambiguous. Options: {', '.join(e.options[:5])}"
    except wikipedia.PageError:
        return "No Wikipedia page found for this query."
    except Exception as e:
        return f"Error fetching Wikipedia data: {str(e)}"


conversation_history = []


def chatboot(prompt):

    conversation_history.append({"role": "user", "content": prompt})

    response = completion(
        model=os.getenv("MODEL"),
        messages=[
            {"role": "system", "content": system_prompt},
            *conversation_history,
        ],
        temperature=0.7,
        max_tokens=1000,
        tool_choice="auto",
        tools=[search_web, search_wikipedia],
    )

    raw_answer = response.choices[0].message.content
    clean_output = clean_think_tags(raw_answer)

    return clean_output
