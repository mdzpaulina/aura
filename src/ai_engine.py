import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def build_master_prompt(metrics_data):
    """
    Takes the clean kubernetes data and formats it into a structured prompt.
    """
    prompt = """
    role: user
    You are AURA (Adaptive Usage and Resource Agent), an expert Oracle Cloud Site Reliability Engineer.
    task: Analyze container consumption metrics
    Your goal is to analyze container consumption metrics in Kubernetes and suggest optimized configurations
    for CPU and Memory 'requests' and 'limits'.

    STRICT RULES:
    1. You must recommend limits that avoid resource waste (cost savings).
    2. You must maintain a 20% safety margin over the current consumption to prevent crashes (OOMKilled).
    3. Respond ONLY with a valid JSON object, with no additional text or Markdown formatting.

    EXPECTED JSON FORMAT:
    {
      "recommendations": [
        {
          "container": "name",
          "new_cpu_limit": 150,
          "new_memory_limit_mb": 256,
          "reasoning": "Brief explanation of the reduction"
        }
      ]
    }

    CURRENT TELEMETRY DATA:
    """
    
    # Convert Python data to a readable string for the model
    data_str = json.dumps(metrics_data, indent=2)
    return prompt + data_str

def analyze_with_aura(metrics_data):
    """
    Sends the prompt to Gemini and returns a Python dictionary with the recommendations.
    """
    if not metrics_data:
        return None

    final_prompt = build_master_prompt(metrics_data)
    
    try:
        # Optimized model for text and code
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # We ask the model to respond strictly in JSON
        response = model.generate_content(
            final_prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        
        # Convert the JSON string back to a Python dictionary
        recommendations_json = json.loads(response.text)
        return recommendations_json
        
    except Exception as e:
        print(f"Error connecting to the AI: {e}")
        return None