
from PIL import Image
import io
import os
import base64
import hashlib


def imghash(image):
    hash = hashlib.sha256()
    hash.update(image.tobytes())
    image_hash = hash.hexdigest()
    return image_hash


def cache(func):
    def wrapper(*args, **kwargs):

        image = args[0]
        image_hash = imghash(image)
        filename = f"app/data/cache/{func.__name__}/img{image_hash}.{(image.format or '.png')}"

        os.makedirs('app/data/cache', exist_ok=True)

        if os.path.exists(filename):
            print("Cache hit.", filename)
            # with open(filename, 'rb') as file:
            #     img = Image.open(file)
            with Image.open(filename) as img:
                result = img

                return result.copy()

        img = func(*args, **kwargs)

        os.makedirs(f'app/data/cache/{func.__name__}', exist_ok=True)
        print("Cache miss. Saving to", filename)
        img.save(filename)

        return img

    return wrapper


def modify_and_encode_image(image_path, cut_height_ratio=0.5):
    """
    Load an image, cut it from the bottom, add empty space below the head,
    preserving the original image size, and encode to Base64.

    :param image_path: Path to the input image.
    :param cut_height_ratio: Ratio of the image height to preserve from the top (0.5 means top 50% is preserved).
    :return: Base64 encoded string of the modified image.
    """
    # Load the image
    with Image.open(image_path) as img:

        # (255, 255, 255)

        # get the background color from top left top corner:
        # background_color = img.getpixel((0, 0))

        # get the background color from the left top corner but slightly below:
        background_color = img.getpixel((0, 10))

        original_size = img.size
        orig_height = 970  # int(0.95 * 1024)  # 20% of the image height
        cut_height = 54  # int(0.05 * 1024)  # 80% of the image height
        # Cut the image from the bottom
        cut_image = img.crop((0, 0, original_size[0], orig_height))

        # Create a new image with the same width and original height, filled with white
        new_image = Image.new('RGB', original_size, background_color)
        new_image.paste(cut_image, (0, cut_height))

        # Convert the image to a bytes object
        img_byte_arr = io.BytesIO()
        new_image.save(img_byte_arr, format=img.format)

        # Encode to Base64
        encoded_image = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

        # save the image:
        # with open("collectibles_v2\\auto_cut.png", 'wb') as file:
        #     file.write(img_byte_arr.getvalue())

    return encoded_image


def encode_by_path(image_path):
    with open(image_path, 'rb') as file:
        data = base64.b64encode(file.read()).decode('utf-8')
        data = f"data:application/octet-stream;base64,{data}"

    return data


def encode_by_img(img):
    img_byte_arr = io.BytesIO()
    # save the image to a byte array in format PNG
    img.save(img_byte_arr, format='PNG')
    encoded_image = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
    return f'data:application/octet-stream;base64,{encoded_image}'


def load_image(image_path):
    # image_path = 'collectibles_v2\\bad.png'
    base64_image = modify_and_encode_image(image_path, cut_height_ratio=0.5)
    base64_image = f'data:application/octet-stream;base64,{base64_image}'
    return base64_image


def encode(img):
    if isinstance(img, str):
        return encode_by_path(img)
    elif isinstance(img, Image.Image):
        return encode_by_img(img)
    else:
        raise ValueError('Invalid input type')


def to_base64(imagepath):
    with open(imagepath, 'rb') as file:
        data = base64.b64encode(file.read()).decode('utf-8')
        data = f"data:application/octet-stream;base64,{data}"
    return data


def convert(x, y):
    # closest possible number  that is divisible by 8 and no less than x
    return x // 8 * 8, y // 8 * 8


@cache
def resize_image_to_multiple_of_8(img):
    print('Resizing image to multiple of 8...', img.size)
    img = img.resize(convert(*img.size))
    print('Resized image to multiple of 8:', img.size)
    return img


@cache
def get_mask(img):
    print('Getting mask...')
    # img = Image.open(img)
    img = img.convert("RGBA")
    datas = img.getdata()
    new_data = []
    for item in datas:
        if item[3] == 0:
            new_data.append((255, 255, 255, 255))
        else:
            new_data.append((0, 0, 0, 255))
    img.putdata(new_data)
    # img.save("mask.png", "PNG")
    return img


# @cache
def resize_image_with_aspect_ratio(image, max_side_length=1024):
    """
    Resize an image while keeping the aspect ratio.

    :param image: Image to resize.
    :param max_side_length: Maximum length of the longer side.
    :return: Resized image.
    """

    print('Resizing image...', image.size)

    # Calculate the new size
    width, height = image.size

    if width <= max_side_length and height <= max_side_length:
        print('Image is already smaller than the max_side_length')
        return image

    if width > height:
        new_width = max_side_length
        new_height = int(height * max_side_length / width)
    else:
        new_height = max_side_length
        new_width = int(width * max_side_length / height)

    resized_image = image.resize((new_width, new_height))
    print('Resized image:', resized_image.size)
    return resized_image


# @cache
def add_white_borders(img, border_width=200):
    width, height = img.size
    white = (255, 255, 255)
    new_width = width + 2 * border_width
    new_height = height + 2 * border_width
    new_img = Image.new('RGB', (new_width, new_height), white)
    new_img.paste(img, (border_width, border_width))

    return new_img


def black_pixels_rate(img):
    black_pixels = 0
    for x in range(img.width):
        for y in range(img.height):
            if img.getpixel((x, y))[:3] == (0, 0, 0):
                black_pixels += 1

            # print(x, y, img.getpixel((x, y)))
    print('Black pixels: {:.2f}%'.format(black_pixels / (img.width * img.height) * 100))
    return black_pixels / (img.width * img.height)


if __name__ == '__main__':
    print(convert(980, 907))  # (980, 904)

    # mask_img = get_mask('app/data/Untitled.png')
    # mask_img.show()
    test_img = Image.open('app/data/Untitled.png')
    resized_img = resize_image_to_multiple_of_8(test_img)
    resized_img.show()
    # img.save('app/data/Untitled_resized.png')
