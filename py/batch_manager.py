import os
import subprocess
from pathlib import Path

# --- CONFIG ---
BASE_DIR = Path(__file__).resolve().parent.parent
PY_DIR = BASE_DIR / "py"
BATCH_DIR = BASE_DIR / "json" / "current_batch"
CONTROLLER = PY_DIR / "controller.py"

def run_single_render(json_file):
    print(f"[PROCESS] Starting render for: {json_file.name}")
    try:
        # Start the process
        proc = subprocess.Popen(
            ["python", str(CONTROLLER), str(json_file)],
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )

        # SET LOW PRIORITY: This prevents the 'Hang'
        p = psutil.Process(proc.pid)
        p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS) 

        stdout, stderr = proc.communicate() # Wait for it to finish
        
        if proc.returncode == 0:
            print(f"[SUCCESS] Completed: {json_file.name}")
            return True
        else:
            print(f"[ERROR] {stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] System Error: {e}")
        return False
    
def process_all_videos():
    # 1. Get all JSON files ready for rendering
    json_files = list(BATCH_DIR.glob("*.json"))
    if not json_files:
        print("[INFO] No batch files found in json/current_batch/")
        return

    print(f"[INFO] Found {len(json_files)} videos in queue.")
    print("[SYSTEM] Mode: Sequential (Safe Mode) - Processing one by one.")

    # 2. Process the list one by one
    success_count = 0
    for f in json_files:
        if run_single_render(f):
            success_count += 1
            
    print(f"\n[SUMMARY] Successfully rendered {success_count} out of {len(json_files)} videos.")

if __name__ == "__main__":
    process_all_videos()