import os
import subprocess
import concurrent.futures
from pathlib import Path

# --- CONFIG ---
BASE_DIR = Path(__file__).resolve().parent.parent
PY_DIR = BASE_DIR / "py"
BATCH_DIR = BASE_DIR / "json" / "current_batch"
CONTROLLER = PY_DIR / "controller.py"

def run_single_render(json_file):
    """Executes the controller for a specific JSON file."""
    print(f"[PROCESS] Starting render for: {json_file.name}")
    try:
        # Run controller as a separate process
        # encoding="utf-8" ensures we can read errors without crashing
        result = subprocess.run(
            ["python", str(CONTROLLER), str(json_file)],
            check=True, 
            capture_output=True, 
            text=True,
            encoding="utf-8"
        )
        return (True, json_file.name)
    except subprocess.CalledProcessError as e:
        return (False, json_file.name, e.stderr)

def process_all_videos():
    # 1. Get all JSON files ready for rendering
    json_files = list(BATCH_DIR.glob("*.json"))
    if not json_files:
        print("[INFO] No batch files found in json/current_batch/")
        return

    print(f"[INFO] Found {len(json_files)} videos in queue.")

    # --- STAGE 1: ATTEMPT PARALLEL PROCESSING ---
    print("\n[STAGE 1] Attempting Parallel Rendering (Speed Mode)...")
    failed_files = []
    
    # We limit max_workers to 3 to prevent RAM exhaustion
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(run_single_render, f): f for f in json_files}
        for future in concurrent.futures.as_completed(futures):
            try:
                success, name, *error = future.result()
                if not success:
                    print(f"[FAILED] Parallel Failed: {name}")
                    failed_files.append(futures[future])
                else:
                    print(f"[SUCCESS] Parallel Success: {name}")
            except Exception as e:
                print(f"[ERROR] Process crashed unexpectedly: {e}")

    # --- STAGE 2: SEQUENTIAL FALLBACK ---
    if failed_files:
        print(f"\n[STAGE 2] {len(failed_files)} renders failed. Switching to Sequential Fallback...")
        for f in failed_files:
            print(f"[RETRY] Retrying {f.name} one-by-one in Safe Mode...")
            success, name, *error = run_single_render(f)
            if success:
                print(f"[SUCCESS] Sequential Success: {name}")
            else:
                print(f"[FATAL] {name} failed even in Safe Mode.")
                if error:
                    print(f"Error Details: {error[0]}")

if __name__ == "__main__":
    process_all_videos()