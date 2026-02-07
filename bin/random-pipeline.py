import subprocess
import re
import time  # optional, for a short delay between runs

def run_script(script_path, *args, capture=False):
    cmd = ["python3", script_path] + list(args)

    if capture:
        result = subprocess.run(cmd, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    else:
        subprocess.run(cmd, check=True, text=True, stdout=None, stderr=None)
        return None

def process_pipeline():
    # Get random words
    words = run_script("bin/get_random_words.py", capture=True)
    print(f"\nRandom words: {words}")

    slug = re.sub(r"[^a-z]+", "-", words.lower()).strip("-")

    # Run your scripts live
    run_script("bin/generate.py", words, f"--destination={slug}-input")
    run_script("bin/img2img.py", f"output/{slug}-input.png", f"--destination={slug}-001")
    time.sleep(60)
    run_script("bin/img2img.py", f"output/{slug}-001.png", f"--destination={slug}-002")
    time.sleep(60)
    run_script("bin/img2img.py", f"output/{slug}-002.png", f"--destination={slug}-003")
    time.sleep(60)

def main():
    print("Starting endless pipeline. Press Ctrl+C to stop.")
    try:
        while True:
            process_pipeline()
    except KeyboardInterrupt:
        print("\nPipeline stopped by user.")

if __name__ == "__main__":
    main()