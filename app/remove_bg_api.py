
import os
if not 'REPLICATE_API_TOKEN' in os.environ:
    from dotenv import load_dotenv
    load_dotenv()

import replicate
from img_utils import *
from PIL import Image


@cache
def rm_bg(image):

    print("Removing background...")
    bs65 = encode(image)

    url = replicate.run(
        "cjwbw/rembg:fb8af171cfa1616ddcf1242c093f9c46bcada5ad4cf6f2fbe8b81b330ec5c003",
        input={
            "image": bs65
        }
    )

    import requests
    print(url)
    response = requests.get(url)

    img = Image.open(io.BytesIO(response.content))
    print("Background removed successfully.")
    return img


if __name__ == '__main__':

    img = rm_bg("app/data/photo_2024-03-21_12-40-25.webp")
    img.show()
