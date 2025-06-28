import torch
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
import os, argparse, time, uuid

parser = argparse.ArgumentParser()
parser.add_argument("image", nargs="?", default="", help="input image", type=os.path.abspath)
parser.add_argument("--size", type=int, default=512, help="image size")
parser.add_argument("--amount", type=int, default=1, help="number of images")
parser.add_argument("--strength", type=float, default=.5, help="how much to change the image")
parser.add_argument("--steps", type=float, default=20, help="num inference steps (quality)")
parser.add_argument("--blur", type=int, default=1, help="blur the input")
parser.add_argument("--guide", type=int, default=12, help="quality guidance")
parser.add_argument("--force", type=bool, default=True, help="prepare to crash")

args = parser.parse_args()

image = args.image
size = args.size
blur = args.blur
strength = args.strength
amount = args.amount
guide = args.guide
force = args.force
steps = args.steps

if force:
    # disable checks on the gpu - may crash your machine
    os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0"
import torch


dirname = os.path.dirname(__file__)
model_folder = os.path.join(dirname, '../model')
output_folder = os.path.join(dirname, '../output')
print(model_folder)
print(output_folder)

# Auto-detect device
device_name = (
    "cuda" if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available()
    else "cpu"
)
device = torch.device(device_name)
torch_dtype = torch.float16 if device_name == "cuda" else torch.float32

# Load base pipeline (no fp16 revision for MPS/CPU!)
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch_dtype,
    safety_checker=None,  # Optional: skip for speed
)

# Move to device
pipe = pipe.to(device)

# Load LoRA weights
pipe.load_lora_weights(model_folder, weight_name="pytorch_lora_weights.safetensors")

# speed up 
pipe.enable_attention_slicing()

# (Optional) fuse LoRA if you want performance (skip if unsure)
pipe.fuse_lora()

# Load your input image
input_image = Image.open(image).convert("RGB").resize((round(size/blur),round(size/blur)))
input_image = input_image.resize((size, size))

# Prompt including LoRA token
prompt = "<skope>"

seed = int(time.time()) 
stamp = f"skope_{uuid.uuid4().hex}"
for i in range(amount):
    generator = torch.Generator(device).manual_seed(seed + i)
    
    # Run img2img
    result = pipe(
        prompt=prompt,
        image=input_image,
        height=size,
        width=size,
        strength=strength,
        guidance_scale=guide,
        num_inference_steps=steps, #25
        generator=generator
    ).images[0]
    filename = stamp+"-"+str(i)+".png"
    filepath = os.path.join(output_folder, filename)

    image.save(filepath)
    print(f"Saved {filepath}")

