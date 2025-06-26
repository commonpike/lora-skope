from diffusers import StableDiffusionPipeline
import torch, glob, uuid, os

# run this for previewing while the training
# is running. it uses cpu to not hog gpu.

dirname = os.path.dirname(__file__)
model_folder = os.path.join(dirname, '../model')
output_folder = os.path.join(dirname, '../output')
filename=f"preview_{uuid.uuid4().hex}.png"
output_file=output_folder+"/"+filename

print(model_folder)
print(output_file)

# img = Image.new("RGB", (64, 64), color="red")
# img.save("output/test.png")

pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5").to("cpu")
latest = sorted(glob.glob(model_folder+"/checkpoint-*"))[-1]
pipe.load_lora_weights(latest)
filename=f"preview_{uuid.uuid4().hex}.png"
# pipe("<stdio_pike> <skope>").images[0].save(output_folder+"/"+filename)
result = pipe("<stdio.pike> <skope> abstract image",height=512,width=512)
if not result.images:
    raise RuntimeError("No images generated")
image = result.images[0]
image = image.copy()  # <- Force copy into safe memory
image.save(output_file)