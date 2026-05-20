import os
import streamlit as st
from groq import Groq

# Try different models
key = os.getenv("GROQ_API_KEY")
if not key:
    print("No key in env, trying hardcoded test")
    
models = ["llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it", "llama-3.3-70b-versatile"]

client = Groq(api_key=key)

for model in models:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=10
        )
        print(f"✅ {model} WORKS")
        break
    except Exception as e:
        print(f"❌ {model} failed: {str(e)[:50]}")
