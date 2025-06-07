"""
一个简单的
将文件夹下所有图片，排序后，一张图片一页 PDF 的输出。
"""

import os
from PIL import Image
from fpdf import FPDF

# 设置包含图片文件的目录和输出PDF的文件名
image_folder = '../data/output'
output_pdf = 'cp-hav-5-2.pdf'

# 创建一个PDF对象
pdf = FPDF()

# 获取文件夹中的所有图片文件并排序
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
image_files.sort()

# 遍历图片文件夹中的所有图片文件
for image_file in image_files:
    # 构建图片文件的完整路径
    image_path = os.path.join(image_folder, image_file)

    # 打开图片文件
    image = Image.open(image_path)

    # 将图片添加到PDF中
    pdf.add_page()
    pdf.image(image_path, x=0, y=0, w=210, h=297)  # A4尺寸：210mm x 297mm

# 将PDF对象写入到新的PDF文件中
pdf.output(output_pdf)

print(f"PDF文件已合并：{output_pdf}")
