from io import BytesIO
import requests
from PIL import Image
from docx.shared import Inches


def download_image(img_url):
    """
    从图床获取图片信息，并返回解析后的数据。
    :param img_url:
    :return:
    """
    print("⏱️ Downloading image from: " + img_url)
    response = requests.get(img_url)
    response.raise_for_status()  # 检查请求是否成功
    image_data = BytesIO(response.content)

    # 使用Pillow库打开图片并获取尺寸
    with Image.open(image_data) as img:
        width, height = img.size
    print("Image size:", width, "x", height)

    return image_data, width, height


def calculate_image_width(image_width, max_image_width_inches, dpi=96):
    """
    计算图片在文档中的适配宽度（EMU）。

    :param image_width: 下载图片函数得到的目标图片宽度。
    :param max_image_width_inches: 最大图片宽度（英寸）
    :param dpi: 每英寸点数，默认为96
    :return: 图片宽度（EMU）
    """
    original_width_inches = image_width / dpi

    # 计算图片的实际宽度（英寸）
    if original_width_inches > max_image_width_inches:
        image_width_inches = max_image_width_inches
    else:
        image_width_inches = original_width_inches

    # 将英寸转换为 EMU，以便插入图片时使用
    image_width_emu = Inches(image_width_inches).emu
    return image_width_emu