from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK

from .utils import *
from .style import cs_lab_report

class DocxHandlerGenerator:
    """
    WHU CS 实验报告 - docx 生成器类。
    """
    dpi = 96
    def __init__(self):
        self.max_image_width_inches = None
        self.document = Document()
        # init
        self.init()
        # Style
        cs_lab_report.set_style(self.document)

    def init(self):
        section = self.document.sections[0]
        page_width = section.page_width
        left_margin = section.left_margin
        right_margin = section.right_margin  # TIP 单位：EMU
        # 计算图片的最大宽度
        max_image_width_emu = page_width - left_margin - right_margin
        self.max_image_width_inches = max_image_width_emu / 914400  # EMU to inches conversion (1 inch = 914400 EMU)

    # INFO 后面都是一些具体的功能函数，
    def add_title(self, idx, title, level):
        """
        添加 CS 要求的标题格式；
        :param idx: 由 MD-AST 计算得出。
        :param title:
        :param level:
        :return:
        """
        if level == 1:
            self.add_page_break()

        # CORE
        pa = self.document.add_paragraph(".".join(str(i) for i in idx), style=f'title-{level}-num')
        # ADD：一个前置空格
        pa.add_run(cs_lab_report.TITLE_MID + title, style=f'title-{level}').bold = True

        # UPDATE 这里有些硬编码
        if level == 1:
            pa.alignment = WD_ALIGN_PARAGRAPH.CENTER

    def add_text(self, text):
        self.document.add_paragraph(cs_lab_report.TEXT_PREFIX + text, style='body')

    def add_picture_with_text(self, idx, img_url, text):
        pa = self.document.add_paragraph()
        run = pa.add_run()
        # 图
        image_data, image_width, image_height = download_image(img_url)
        run.add_picture(image_data, width=calculate_image_width(image_width, self.max_image_width_inches, self.dpi))
        pa.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # 图例文本
        pa = self.document.add_paragraph(cs_lab_report.IMG_TEXT_PREFIX, style='img-title')
        pa.add_run(".".join(str(i) for i in idx), style='img-title-num').bold = True
        pa.add_run(cs_lab_report.IMG_TEXT_MID + text, style='img-title-2')
        pa.alignment = WD_ALIGN_PARAGRAPH.CENTER

    def add_page_break(self):
        self.document.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    def save(self, filename):
        self.document.save(filename)


if __name__ == '__main__':
    docx_handler = DocxHandlerGenerator()
    docx_handler.add_title([2], '这是一个标题', 1)
    docx_handler.add_title([1, 1], "H2", 2)
    docx_handler.add_text(
        "测试文本段覅哦沙发第四哦分段覅哦沙发第四哦分段覅哦沙发第四哦分，段覅哦沙发第四哦分段覅哦沙发第四哦分。")

    docx_handler.add_picture_with_text([1, 1], "https://www.helloimg.com/i/2024/12/25/676b92d11041e.png", "测试图片")

    docx_handler.save('example.docx')
