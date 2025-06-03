#!/bin/bash

BASEDIR=`dirname $0`/..

INPUTDIR=$BASEDIR/input
echo "Input data: $INPUTDIR"

TRAINDIR="$BASEDIR/model"
echo "Training destination: $TRAINDIR"

CHECKPOINTS=$(ls -d $TRAINDIR/checkpoint-* 2>/dev/null)
if [ -n "$CHECKPOINTS" ]; then
  echo "Checkpoints found, resuming from latest."
  RESUME_ARG="--resume_from_checkpoint=latest"
else
  echo "No checkpoints found, starting fresh."
  RESUME_ARG=""
fi

 # (optional) lift VRAM cap
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0  


accelerate launch diffusers/examples/dreambooth/train_dreambooth_lora.py \
  --pretrained_model_name_or_path="runwayml/stable-diffusion-v1-5" \
  --instance_data_dir="$INPUTDIR" \
  --instance_prompt="<stdio.pike> <skope>" \
  --resolution=512 \
  --train_batch_size=1 \
  --num_train_epochs=2 \
  --learning_rate=1e-4 \
  --output_dir="$TRAINDIR" \
  --checkpointing_steps=50 \
  --gradient_checkpointing \
  --report_to="tensorboard" \
  $RESUME_ARG
#  --max_train_steps=800 \
#  --enable_xformers_memory_efficient_attention \ # fails on m1
#  --mixed_precision="fp16" \ #not on apple gpu
