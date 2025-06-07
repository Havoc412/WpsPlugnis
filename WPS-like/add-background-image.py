from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO

# 添加带有透明度的背景图片
def create_background_pdf(page_width, page_height, img_path):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))

    # 加载图片
    img = ImageReader(img_path)
    img_width, img_height = img.getSize()

    # 计算图片的宽高比和页面的宽高比
    img_aspect_ratio = img_width / img_height
    page_aspect_ratio = page_width / page_height

    # 调整图片大小以适应页面
    if img_aspect_ratio > page_aspect_ratio:  # 图片宽高比大于页面宽高比
        new_width = page_width
        new_height = page_width / img_aspect_ratio
    else:  # 图片宽高比小于或等于页面宽高比
        new_height = page_height
        new_width = page_height * img_aspect_ratio

    # 计算图片居中位置
    x_offset = (page_width - new_width) / 2
    y_offset = (page_height - new_height) / 2

    # 设置透明度
    can.saveState()
    can.setFillAlpha(0.2)  # 设置透明度为0.2
    can.drawImage(img, x_offset, y_offset, width=new_width, height=new_height)
    can.restoreState()

    can.save()
    packet.seek(0)
    return packet

# 主函数
def add_background_to_pdf(input_pdf_path, output_pdf_path, img_path):
    # 读取原始 PDF
    original_pdf = PdfReader(input_pdf_path)
    output_pdf = PdfWriter()

    # 为每一页添加背景图片
    for i in range(len(original_pdf.pages)):
        page = original_pdf.pages[i]
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)

        # 创建背景 PDF
        background_pdf_packet = create_background_pdf(page_width, page_height, img_path)
        background_pdf = PdfReader(background_pdf_packet)

        # 合并背景和原始页面
        page.merge_page(background_pdf.pages[0])
        output_pdf.add_page(page)

    # 保存最终 PDF
    with open(output_pdf_path, "wb") as outputStream:
        output_pdf.write(outputStream)


if __name__ == "__main__":
    input_pdf_path = r"C:\Users\Havoc\Desktop\bb5cb052621074b4426998fcfeee100b.pdf"
    output_pdf_path = "output.pdf"
    img_path = r"C:\Users\Havoc\Desktop\980.jpg"
    add_background_to_pdf(input_pdf_path, output_pdf_path, img_path)
