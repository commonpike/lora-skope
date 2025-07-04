# LoRA-Skope: Minimal Stable Diffusion LoRA Training & Inference

This repo trains a [LoRA](https://arxiv.org/abs/2106.09685) adapter for `runwayml/stable-diffusion-v1-5`, using my own custom image dataset — and generates images with it. Designed to run locally or on another machine with a compatible GPU.

---

## License 

https://ai.meta.com/llama/license/

Licensed under the LLaMA-style Community License:
- You may download and use these weights *only for non-commercial research purposes*.
- Any other use (inference, commercial, distribution) requires my prior written permission.

## Project Structure

```
├── bin/ # Python + shell scripts for training and preview
├── input/ # Put your training images here (optional .gitkeep for sharing)
├── output/ # Generated images go here
├── model/ # Stores your LoRA training output (can include in repo)
├── README.md # You're reading it
├── requirements.txt # Recreate the Python environment
└── .gitignore # Ignore local env and outputs
```

---

## Quick Start

### Create the Environment

```bash
# set up virtual environment
python3 -m venv lora-env
source lora-env/bin/activate

# optional: install pip
curl https://bootstrap.pypa.io/get-pip.py -o bin/get-pip.py
python bin/get-pip.py

# let pip install requirements
pip install -r requirements.txt

git clone https://github.com/huggingface/diffusers.git
cd diffusers
pip install -e .  # Optional, installs editable version
```

### Train

```
source lora-env/bin/activate
bin/train.sh
```

### Generate

```
source lora-env/bin/activate
python3 bin/generate.py
```

### Notes

- If you move the repo around, you have to rebuild the env; that's just python.

