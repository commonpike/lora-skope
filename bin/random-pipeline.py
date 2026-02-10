import os
import subprocess
import re
import time  # optional, for a short delay between runs
from wonderwords import RandomWord
from datetime import datetime

def run_script(script_path, *args, capture=False):
    cmd = ["python3", script_path] + list(args)

    if capture:
        result = subprocess.run(cmd, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    else:
        subprocess.run(cmd, check=True, text=True, stdout=None, stderr=None)
        return None

def process_pipeline():
    # get date
    # current date
    today = datetime.today()

    # format as YYYYMMDD
    yyyymmdd = today.strftime("%Y%m%d")

    # Get random words
    rw = RandomWord()
    words_array = rw.random_words(2)
    words = " ".join(words_array)
    slug = re.sub(r"[^a-z]+", "-", words.lower()).strip("-")

    # make dir and write body 
    os.makedirs(f"output/{yyyymmdd}-{slug}", exist_ok=True)
    with open(f"output/{yyyymmdd}-{slug}/body.txt", "w") as body:
        body.write(f"{words.title()}\n\n#cgi #skope #blender #stable-diffusion")

    print("words:" + words)
    print("output:" + f"{yyyymmdd}-{slug}")

    # Run your scripts live
    for name in [slug+"-001",slug+"-002",slug+"-003",slug+"-004"]:
        run_script("bin/generate.py", words, "--skope=1.0", f"--destination={yyyymmdd}-{slug}/_{name}-org")
        time.sleep(60)
        run_script("bin/img2img.py", f"output/{yyyymmdd}-{slug}/_{name}-org.png", f"--destination={yyyymmdd}-{slug}/_{name}-A")
        time.sleep(60)
        run_script("bin/img2img.py", f"output/{yyyymmdd}-{slug}/_{name}-A.png", f"--destination={yyyymmdd}-{slug}/_{name}-B")
        time.sleep(60)
        run_script("bin/img2img.py", f"output/{yyyymmdd}-{slug}/_{name}-B.png", f"--destination={yyyymmdd}-{slug}/{name}")
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