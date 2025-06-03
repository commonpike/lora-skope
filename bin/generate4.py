from diffusers import StableDiffusionPipeline
from peft      import PeftModel
import torch, uuid, os

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
    #torch_dtype=torch.float16         # Optional: use less memory
)

# Load your trained LoRA weights
pipe.load_lora_weights(training_folder)

# Use the Apple Silicon GPU if available
device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
pipe = pipe.to(device)

# ----------------------------------------------------------------------------------
# 2.  Generate images
# ----------------------------------------------------------------------------------
prompt      = "stdio.pike skope"
num_images  = 10
out_dir     = output_folder          # images will be saved here
os.makedirs(out_dir, exist_ok=True)

for _ in range(num_images):
    # image = pipe(prompt).images[0]
    seed = 42  # Or any fixed number
    generator = torch.manual_seed(seed)
    images = pipe(
        prompt, 
        num_images_per_prompt=4, 
        #guidance_scale=7.5, # default=12 
        #height=64,
        #width=64
        generator=[generator.manual_seed(seed + i) for i in range(4)]
    ).images

    # Create a random, unique filename with UUID-4
    stamp=f"skope_{uuid.uuid4().hex}"
    for i, image in enumerate(images):
      filename = stamp+"-"+str(i)+".png"
      filepath = os.path.join(out_dir, filename)

      image.save(filepath)
      print(f"Saved {filepath}")
