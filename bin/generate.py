from diffusers import StableDiffusionPipeline
from peft      import PeftModel
import time, uuid, os, argparse

parser = argparse.ArgumentParser()
parser.add_argument("prompt", nargs="?", default="", help="optional prompt")
parser.add_argument("--size", type=int, default=512, help="image size")
parser.add_argument("--groups", type=int, default=1, help="number of groups")
parser.add_argument("--amount", type=int, default=1, help="number of images per group")
parser.add_argument("--guide", type=int, default=12, help="quality guidance")
parser.add_argument("--force", type=bool, default=True, help="prepare to crash")
parser.add_argument("--restyle", type=float, default=1.0, help="factor of custom restyling")

args = parser.parse_args()

prompt = args.prompt
size = args.size
groups = args.groups
amount = args.amount
guide = args.guide
force = args.force
restyle = args.restyle

if force:
    # disable checks on the gpu - may crash your machine
    os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0"
import torch

dirname = os.path.dirname(__file__)
model_folder = os.path.join(dirname, '../model')
output_folder = os.path.join(dirname, '../output')
print(model_folder)
print(output_folder)

# ----------------------------------------------------------------------------------
# 1. Load base Stable Diffusion and your LoRA adapter
# ----------------------------------------------------------------------------------

base_model_id = "runwayml/stable-diffusion-v1-5"
device_name = (
    "cuda" if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available()
    else "cpu"
)

# Load the base model
pipe = StableDiffusionPipeline.from_pretrained(
    base_model_id,
    safety_checker=None,              # Optional: disable NSFW safety checker
    torch_dtype=torch.float16 if device_name != "cpu" else torch.float32   # Optional: use less memory
)

# Load your trained LoRA weights
pipe.load_lora_weights(model_folder)

# Use the Apple Silicon GPU if available
device = torch.device(device_name)
pipe = pipe.to(device)

# ----------------------------------------------------------------------------------
# 2.  Generate images
# ----------------------------------------------------------------------------------
prompt_add  = "" # "abstract image"
prompt      = f"<skope> {prompt_add} ({prompt}:{1/restyle})"
print("prompt:" + prompt)

os.makedirs(output_folder, exist_ok=True)

for _ in range(groups):
    # image = pipe(prompt).images[0]
    seed = int(time.time()) 
    stamp = f"skope_{uuid.uuid4().hex}"
    for i in range(amount):
        generator = torch.Generator(device).manual_seed(seed + i)
        image = pipe(
            prompt, 
            guidance_scale=guide,
            height=size,
            width=size,
            generator=generator
        ).images[0]

        filename = stamp+"-"+str(i)+".png"
        filepath = os.path.join(output_folder, filename)

        image.save(filepath)
        print(f"Saved {filepath}")
