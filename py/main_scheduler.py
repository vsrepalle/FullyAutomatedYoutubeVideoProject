import os
import json
import time
from datetime import datetime
from pathlib import Path
import integrate_grok
import controller
import batch_manager
from dotenv import load_dotenv

# --- PATH SETUP ---
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
config_path = BASE_DIR / "json" / "automation_config.json"
load_dotenv(dotenv_path=env_path)

class Log:
    HEADER = '\033[95m[SYSTEM]\033[0m'
    CLOCK = '\033[96m[TIME]\033[0m'
    SUCCESS = '\033[92m[DONE]\033[0m'

def run_automation_cycle(channel_name, topic):
    print(f"\n{Log.HEADER} Starting Cycle for: {channel_name}")
    
    # 1. Fetch from Groq (using your integrate_grok logic)
    json_data = integrate_grok.get_ai_answer(channel_name, topic)
    
    if json_data:
        # 2. Save the JSON data
        filepath = integrate_grok.process_and_save(json_data, channel_name)
        
        if filepath:
            print(f"{Log.SUCCESS} JSON Data Ready. Handing over to Batch Manager...")
            # 3. Trigger Rendering (Parallel with Sequential Fallback)
            batch_manager.process_all_videos()
            
            # 4. [COMING SOON] Persistent Auth & Upload logic
            # upload_to_youtube(channel_name)
    else:
        print(f"❌ Cycle failed for {channel_name}: No AI response.")

def main():
    print(f"{Log.HEADER} GEMINI-CORE AUTONOMOUS SCHEDULER ACTIVE")
    last_run_minute = ""

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        # Avoid running multiple times in the same minute
        if current_time != last_run_minute:
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)

                for name, data in config['channels'].items():
                    # Check if current time matches any scheduled slot
                    if current_time in data.get('schedule', []):
                        print(f"{Log.CLOCK} Slot Match Found: {current_time} for {name}")
                        topic = data.get('prompt_logic', "Latest news")
                        run_automation_cycle(name, topic)
                        last_run_minute = current_time

            except Exception as e:
                print(f"❌ Scheduler Error: {e}")
        
        # Sleep to save CPU; check every 30 seconds
        time.sleep(30)

if __name__ == "__main__":
    main()