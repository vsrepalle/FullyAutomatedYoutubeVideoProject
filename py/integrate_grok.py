import os
import json
import sys
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

# --- 1. PATH SETUP ---
# Resolves the root directory regardless of where you run the script from
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
config_path = BASE_DIR / "json" / "automation_config.json"

# Load environment variables
load_dotenv(dotenv_path=env_path)

# --- 2. LOGGER CLASS ---
class Log:
    INFO = '\033[94m[INFO]\033[0m'
    SUCCESS = '\033[92m[SUCCESS]\033[0m'
    ERROR = '\033[91m[ERROR]\033[0m'
    WARN = '\033[93m[WARN]\033[0m'
    DEBUG = '\033[95m[DEBUG]\033[0m'

# --- 3. AI ENGINE (GROQ FREE TIER) ---
def get_ai_answer(channel, user_topic):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print(f"{Log.ERROR} GROQ_API_KEY not found. Check your .env at: {env_path}")
        return None

    client = Groq(api_key=api_key)
    
    # Using Llama 3.3 70B for high-quality English news/facts
    model_name = "llama-3.3-70b-versatile"
    
    system_prompt = (
        f"You are the autonomous engine for {channel}. Output ONLY a raw JSON array. "
        "Rules: 1. Use English only. 2. Every scene MUST have 'hook_text'. "
        "3. End 'details' with 'Tune with us for more such news'. "
        "4. Follow the specific brand voice for cricket, bollywood, or wonders."
    )

    try:
        print(f"{Log.INFO} Querying {model_name} for topic: {user_topic}...")
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create 4 scenes about: {user_topic}"}
            ],
            temperature=0.2
        )
        
        raw_content = completion.choices[0].message.content
        
        # CLEANING LOGIC: Extract only the JSON array
        start_index = raw_content.find("[")
        end_index = raw_content.rfind("]") + 1
        
        if start_index != -1 and end_index != 0:
            return raw_content[start_index:end_index]
        return raw_content

    except Exception as e:
        print(f"{Log.ERROR} Groq API Error: {str(e)}")
        return None

# --- 4. DATA PROCESSOR ---
def process_and_save(json_str, channel_name):
    try:
        data = json.loads(json_str)
        
        # Ensure 'current_batch' directory exists
        output_dir = BASE_DIR / "json" / "current_batch"
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{channel_name}_latest.json"
        filepath = output_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            
        print(f"{Log.SUCCESS} Saved {len(data)} scenes to {filepath}")
        return filepath
    except Exception as e:
        print(f"{Log.ERROR} Failed to parse or save JSON: {e}")
        return None

# --- 5. MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    print(f"\n{Log.DEBUG} --- 🤖 GEMINI-CORE INTEGRATION STARTED ---")
    
    # 1. Verify environment
    if os.path.exists(env_path):
        print(f"{Log.INFO} Found .env at: {env_path}")
    else:
        print(f"{Log.WARN} .env file missing at expected location!")

    # 2. Example Test Run (e.g., WonderFacts)
    test_channel = "WonderFacts24_7"
    test_topic = "Deep Sea Creatures that glow in the dark"
    
    content = get_ai_answer(test_channel, test_topic)
    
    if content:
        save_path = process_and_save(content, test_channel)
        if save_path:
            print(f"{Log.SUCCESS} Integration Test Complete! Ready for Controller.")
    else:
        print(f"{Log.ERROR} Integration Test Failed. No content generated.")

    print(f"{Log.DEBUG} --- 🏁 SYSTEM IDLE ---\n")
    # input("Press Enter to exit...") # Optional: keeps window open