import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # reads GROQ_API_KEY from backend/.env

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

resume_text = """
B.Tech CSE 2025. Skills: C++, Python, FastAPI, React, SQL.
Built a RAG engine with Llama 3.2 and a resume analyzer.
"""

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "system",
            "content": "You extract data from resumes. Return only JSON with keys: skills (list of strings), education (string).",
        },
        {"role": "user", "content": resume_text},
    ],
    response_format={"type": "json_object"},
)

print(response.choices[0].message.content)