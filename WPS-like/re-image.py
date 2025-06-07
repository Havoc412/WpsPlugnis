from PIL import Image
import os

def compress_image(input_path, output_path, quality=85, optimize=True, format="JPEG"):
    """
    Compresses an image file to a given quality.

    :param input_path: Path to the input image file.
    :param output_path: Path to save the compressed image file.
    :param quality: Compression quality (2-100), default is 85.
    :param optimize: Whether to optimize the image file size, default is True.
    :param format: Output image format, default is "JPEG".
    """
    # Open the input image
    with Image.open(input_path) as img:
        # Convert image to RGB mode if it's not already
        if img.mode != "RGB":
            img = img.convert("RGB")

        # Save the image with the specified quality and format
        img.save(output_path, format=format, quality=quality, optimize=optimize)

def batch_compress_images(input_folder, output_folder, quality=85, optimize=True, format="JPEG"):
    """
    Compresses all images in the input folder and saves them to the output folder.

    :param input_folder: Path to the folder containing input images.
    :param output_folder: Path to the folder where compressed images will be saved.
    :param quality: Compression quality (2-100), default is 85.
    :param optimize: Whether to optimize the image file size, default is True.
    :param format: Output image format, default is "JPEG".
    """
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            compress_image(input_path, output_path, quality, optimize, format)

# Example usage
input_folder = "../data"
output_folder = os.path.join(input_folder, "output")
batch_compress_images(input_folder, output_folder, quality=70, optimize=True, format="JPEG")
