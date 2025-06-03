from diffusers import StableDiffusionPipeline
from peft      import PeftModel
import uuid, os
# disable checks on the gpu - may crash your machine
os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0"
import torch

dirname = os.path.dirname(__file__)
training_folder = os.path.join(dirname, '../output_lora')
output_folder = os.path.join(dirname, '../output')
print(training_folder)
print(output_folder)

# ----------------------------------------------------------------------------------
# 1. Load base Stable Diffusion and your LoRA adapter
# ----------------------------------------------------------------------------------

base_model_id = "runwayml/stable-diffusion-v1-5"

# Load the base model
pipe = StableDiffusionPipeline.from_pretrained(
    base_model_id,
    safety_checker=None,              # Optional: disable NSFW safety checker
    torch_dtype=torch.float16         # Optional: use less memory
)

# Load your trained LoRA weights
pipe.load_lora_weights(training_folder)

# Use the Apple Silicon GPU if available
device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
pipe = pipe.to(device)

# ----------------------------------------------------------------------------------
# 2.  Generate images
# ----------------------------------------------------------------------------------
prompt      = "<stdio.pike> <skope>"
num_images  = 10
os.makedirs(output_folder, exist_ok=True)

for _ in range(num_images):
    image = pipe(
        prompt,
        guidance_scale=7.5, # default=12 
        height=256,
        width=256
    ).images[0]

    # Create a random, unique filename with UUID-4
    filename = f"skope_{uuid.uuid4().hex}.png"
    filepath = os.path.join(output_folder, filename)

    image.save(filepath)
    print(f"Saved {filepath}")
