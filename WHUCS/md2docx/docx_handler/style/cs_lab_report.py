from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn

"""
# QUES ‘2’级 bold 无效；需要代码里设定。
"""


TITLE_MID = " "
TEXT_PREFIX =  "    "
IMG_TEXT_PREFIX = "图"
IMG_TEXT_MID = " "


def set_style(document: Document):
    """ Title """
    # H1（黑体小2）
    style_title_1 = document.styles.add_style('title-1', 2)
    style_title_1.font.name = '黑体'
    style_title_1._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    style_title_1.font.size = Pt(18)

    # BUG 居中写到这里看起来是无效。
    # style_title_1.alignment = WD_ALIGN_PARAGRAPH.CENTER

    style_title_1_num = document.styles.add_style('title-1-num', 1)
    style_title_1_num.font.name = 'Times New Roman'
    style_title_1_num._element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
    style_title_1_num.font.size = Pt(18)
    style_title_1_num.font.bold = True

    # H2（黑体4号）
    style_title_2 = document.styles.add_style('title-2', 2)
    style_title_2.font.name = '黑体'
    style_title_2._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    style_title_2.font.size = Pt(14)

    style_title_2_num = document.styles.add_style('title-2-num', 1)
    style_title_2_num.font.name = 'Times New Roman'
    style_title_2_num._element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
    style_title_2_num.font.size = Pt(14)
    style_title_2_num.font.bold = True

    """ Body """
    # 正文（宋体小四、行距23p）
    style_body = document.styles.add_style('body', 1)
    style_body.font.name = '宋体'
    style_body._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    style_body.font.size = Pt(12)
    style_body.paragraph_format.line_spacing = Pt(23)  # 行距23磅

    """ IMG / Table """
    style_img_title = document.styles.add_style('img-title', 1)
    style_img_title.font.name = '黑体'
    style_img_title._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    style_img_title.font.size = Pt(12)

    style_img_title_2 = document.styles.add_style('img-title-2', 2)
    style_img_title_2.font.name = '黑体'
    style_img_title_2._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    style_img_title_2.font.size = Pt(12)

    style_img_title_num = document.styles.add_style('img-title-num', 2)
    style_img_title_num.font.name = 'Times New Roman'
    style_img_title_num._element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
    style_img_title_num.font.size = Pt(12)



