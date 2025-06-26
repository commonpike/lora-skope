# LoRA-Skope: Minimal Stable Diffusion LoRA Training & Inference

This repo trains a [LoRA](https://arxiv.org/abs/2106.09685) adapter for `runwayml/stable-diffusion-v1-5`, using your own custom image dataset — and generates images with it. Designed to run locally or on another machine with a compatible GPU.

---

## License 

https://ai.meta.com/llama/license/

Licensed under the LLaMA-style Community License:
- You may download and use these weights *only for non-commercial research purposes*.
- Any other use (inference, commercial, distribution) requires my prior written permission.

## Project Structure

├── bin/ # Python + shell scripts for training and preview
├── input/ # Put your training images here (optional .gitkeep for sharing)
├── output/ # Generated images go here
├── model/ # Stores your LoRA training output (can include in repo)
├── README.md # You're reading it
├── requirements.txt # Recreate the Python environment
└── .gitignore # Ignore local env and outputs

---

## Quick Start

### Create the Environment

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

git clone https://github.com/huggingface/diffusers.git
cd diffusers
pip install -e .  # Optional, installs editable version
```

### Train

```
bin/train.sh
```

### Generate

```
python bin/generate.py
```

