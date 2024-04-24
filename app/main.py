

from remove_bg_api import rm_bg
from sdxl_api import inpaint
from img_utils import *

import requests
import os
import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--source_folder', type=str, help='source folder')
    sources_folder = parser.parse_args().source_folder

    for img_name in os.listdir(sources_folder):

        img_path = f'{sources_folder}/{img_name}'
        img_orig = Image.open(img_path)

        optimal_img = resize_image_with_aspect_ratio(img_orig)  # FIX FOR: replicate.exceptions.ModelError: CUDA out of memory. Tried to allocate 5.80 GiB (GPU 0; 47.54 GiB total capacity; 34.98 GiB already allocated; 923.88 MiB free; 46.29 GiB reserved in total by PyTorch) If reserved memory is >> allocated memory try setting max_split_size_mb to avoid fragmentation.  See documentation for Memory Management and PYTORCH_CUDA_ALLOC_CONF
        optimal_img = resize_image_to_multiple_of_8(optimal_img)

        no_bg_img = rm_bg(optimal_img)
        mask_img = get_mask(no_bg_img)

        if black_pixels_rate(mask_img) > 0.5:
            optimal_img = add_white_borders(img_orig, border_width=optimal_img.width // 2)
            optimal_img = resize_image_with_aspect_ratio(img_orig)
            optimal_img = resize_image_to_multiple_of_8(optimal_img)

            no_bg_img = rm_bg(optimal_img)
            mask_img = get_mask(no_bg_img)

        prompt = "catalog-photo, wooden floor, green-walls background, object-photo, photo-realistic, ultra-hd, hd, object-photography, still-life"

        width, height = mask_img.size

        print('original size:', optimal_img.size)
        print('mask size:', mask_img.size)

        redrawn_imgs = inpaint(
            optimal_img,
            mask_img,
            prompt,
            width,
            height
        )

        for i, url in enumerate(redrawn_imgs):
            os.makedirs('app/data/results', exist_ok=True)

            response = requests.get(url)
            result_img = Image.open(io.BytesIO(response.content))
            result_img.save(f'app/data/results/{img_name}_{i}.png')
            print(f"Saved {img_name}.")
        print(f"Done with {img_name}.\n\n")
