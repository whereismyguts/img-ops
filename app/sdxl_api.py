import replicate

from img_utils import *

import os
if not 'REPLICATE_API_TOKEN' in os.environ:
    from dotenv import load_dotenv
    load_dotenv()

NP = 'blurry, blur, text, watermark, render, 3D, NSFW, nude, CGI, monochrome, B&W, cartoon, painting, smooth, plastic, blurry, low-resolution, deep-fried, oversaturated, details, white, empty, none'


def inpaint(image, mask, prompt, width, height, negative_prompt=None):

    print("Inpainting...")
    output = replicate.run(
        "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        input={
            "mask": encode(mask),
            "image": encode(image),
            "width": width,
            "height": height,
            "prompt": prompt or '',
            "negative_prompt": negative_prompt or NP,
            "refine": "expert_ensemble_refiner",
            "scheduler": "K_EULER",
            "lora_scale": 0.6,
            "num_outputs": 4,
            "guidance_scale": 7.5,
            "apply_watermark": False,
            "high_noise_frac": 0.8,
            "prompt_strength": 0.9,
            "num_inference_steps": 30
        },
    )
    print("Inpainting done")
    print(output)
    return output
