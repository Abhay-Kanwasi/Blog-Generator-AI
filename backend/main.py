from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
import logging

# Load environment variable
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Blog Generator API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get API keys from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

class BlogRequest(BaseModel):
    topic: str
    tone: str = "formal"
    apiProvider: str

class BlogResponse(BaseModel):
    content: str
    status: str = "success"
    

@app.post("/generate", response_model=BlogResponse)
async def generate_blog(request: BlogRequest):
    if not request.topic:
        raise HTTPException(status_code=400, detail="Topic is required")
    
    # Decide which API to use (Groq is default)
    api_choice = request.apiProvider.lower()
    
    try:
        if api_choice == "huggingface":
            return await generate_with_huggingface(request)
        else:
            return await generate_with_groq(request)
    except Exception as e:
        logger.error(f"Error generating blog: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate blog: {str(e)}")

async def generate_with_groq(request: BlogRequest):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ API key not configured")
    print("groq")
    # Prepare prompt for Groq
    prompt = f"""
    Write a well-structured, engaging, and informative blog post about {request.topic} in a {request.tone} tone.

    The blog should:
        Start with a compelling hook that grabs the reader’s attention and introduces the topic in a relatable way.
        Be well-structured with clear, engaging headings and smooth transitions between sections.
        Provide valuable insights, practical advice, or actionable takeaways that keep the reader interested and informed.
        Use storytelling, examples, or real-world applications to make the content more engaging and relatable.
        Maintain a conversational yet authoritative tone to establish credibility while keeping the reader engaged.
        End with a strong conclusion, summarizing key points and encouraging further thought or action.
        Make the content immersive, easy to read, and valuable for the target audience.
    """
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-70b-8192",  # Or use another model like "mixtral-8x7b-32768"
                "messages": [
                    {"role": "system", "content": "You are an expert blog writer who creates engaging, well-researched content."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
        )
        
        if response.status_code != 200:
            logger.error(f"Groq API error: {response.text}")
            raise HTTPException(status_code=response.status_code, detail="Error from Groq API")
            
        result = response.json()
        blog_content = result["choices"][0]["message"]["content"]
        
        return BlogResponse(content=blog_content)

async def generate_with_huggingface(request: BlogRequest):
    if not HF_API_KEY:
        raise HTTPException(status_code=500, detail="Hugging Face API key not configured")
    print('HF')
    # Define the model to use (can be configured in .env)
    model_id = os.getenv("HF_MODEL_ID", "mistralai/Mistral-7B-Instruct-v0.2")
    
    # Prepare prompt for Hugging Face
    prompt = f"""<s>[INST] Write a well-structured, engaging blog post about {request.topic} in a {request.tone} tone.
    
    The blog should include:
    - An attention-grabbing introduction
    - Well-organized body paragraphs with relevant headings
    - Practical insights or actionable tips when applicable
    - A compelling conclusion
    
    Make it informative yet engaging for the reader. [/INST]</s>
    """
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"https://api-inference.huggingface.co/models/{model_id}",
            headers={"Authorization": f"Bearer {HF_API_KEY}"},
            json={"inputs": prompt, "parameters": {"max_new_tokens": 2000, "temperature": 0.7}}
        )
        
        if response.status_code != 200:
            logger.error(f"Hugging Face API error: {response.text}")
            raise HTTPException(status_code=response.status_code, detail="Error from Hugging Face API")
            
        result = response.json()
        
        # Extract content based on response format (may vary by model)
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], dict) and "generated_text" in result[0]:
                blog_content = result[0]["generated_text"]
            else:
                blog_content = result[0]
        elif isinstance(result, dict) and "generated_text" in result:
            blog_content = result["generated_text"]
        else:
            blog_content = str(result)
            
        # Clean up the response if needed
        if "<s>[INST]" in blog_content:
            blog_content = blog_content.split("[/INST]</s>")[-1].strip()
        
        return BlogResponse(content=blog_content)

@app.get("/")
async def read_root():
    return {"status": "API is running", "endpoints": ["/generate"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)