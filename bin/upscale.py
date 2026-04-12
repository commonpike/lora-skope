import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 1. Setup Client
client = genai.Client(api_key=api_key)

prompt = "Expand this image to 2048x2048, creatively adding details that match the original style."

with open("output/skope_750ad9cf9834452eae85ac57a658bbc8.png", "rb") as f:
    img_bytes = f.read()

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        prompt,
        types.Part.from_bytes(
            data=img_bytes,
            mime_type="image/png"
        )
    ]
)

# extract image
for part in response.candidates[0].content.parts:
    if getattr(part, "inline_data", None):
        with open("upscaled.png", "wb") as f:
            f.write(part.inline_data.data)

print("Done → upscaled.png")