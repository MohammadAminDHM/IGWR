from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def enhance_prompt(user_prompt, model_name, system_prompt):
    """Prompt Reflection"""
    api_key = os.getenv("AVALAI_API_KEY")
    base_url = os.getenv("BASE_URL")
    
    if not api_key or not base_url:
        raise ValueError("Missing required environment variables: OPENAI_API_KEY and/or BASE_URL")
    
    system_message = system_prompt
    
    try:
        llm = ChatOpenAI(
            model_name=model_name,
            base_url=base_url,
            api_key=api_key
        )                      
        
        response = llm.invoke([
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ])
        
        return response.content.strip()
    except Exception as e:
        raise Exception(f"Error during prompt enhancement: {str(e)}")
