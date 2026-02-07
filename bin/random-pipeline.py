import subprocess
import re

def get_word():
    result = subprocess.run(
        ["python3", "get_random_word.py"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()

def run_script(script_name, word):
    result = subprocess.run(
        ["python3", script_name, word],
        check=True,
    )
    return result.stdout.strip()

def main():
    words = run_script("get_random_words.py").strip()
    print(f"Random words: {words}")

    # clean, stable slug
    slug = re.sub(r"[^a-z]+", "-", words.lower()).strip("-")

    run_script(
        "bin/generate.py",
        words,
        f"--destination={slug}-input",
    )

    run_script(
        "bin/img2img.py",
        f"{slug}-input.png",
        f"--destination={slug}-001",
    )

    run_script(
        "bin/img2img.py",
        f"{slug}-001.png",
        f"--destination={slug}-002",
    )

    run_script(
        "bin/img2img.py",
        f"{slug}-002.png",
        f"--destination={slug}-003",
    )
    
if __name__ == "__main__":
    main()