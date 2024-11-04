# main.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import os
from together import Together  # Ensure 'together' package is installed
from dotenv import load_dotenv
import os

# Load environment variables from .env fileS
load_dotenv()

app = FastAPI()

# Initialize Together client
key = os.getenv('TOGETHER_API_KEY') 

client = Together(api_key=key)

class Query(BaseModel):
    user_input: str

def create_summarization_prompt(element: str) -> str:
    """Create a prompt for summarizing user input in a medical context."""
    prompt_text = (
        f"""You are a medical assistant that provides medical advice to users and helps them if they are feeling depressed. Please behave professionally as a doctor and therapist. {element}"""
    )
    return prompt_text

def summarize_element_with_together(element: str) -> str:
    """Send prompt to Together's API for a response."""
    summarization_prompt = create_summarization_prompt(element)

    # Request to Together API
    response = client.chat.completions.create(
        model="meta-llama/Llama-Vision-Free",
        messages=[
            {"role": "user", "content": summarization_prompt}
        ]
    )

    # Return the response content
    return response.choices[0].message.content

@app.post("/ask")
def ask_question(query: Query):
    """Endpoint to take user query and return the generated response."""
    if not query.user_input:
        raise HTTPException(status_code=400, detail="Input query cannot be empty")
    
    try:
        answer = summarize_element_with_together(query.user_input)
        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app. Use /ask to submit your query."}
