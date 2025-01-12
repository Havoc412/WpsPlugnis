import os
import PyPDF2

"""
由于 WPS 会员要求，怒而自写，一刻钟足以。
By Havoc 🐱
"""


def parse_page_ranges(page_string):
    page_list = []
    ranges = page_string.split(',')

    for range_str in ranges:
        if '-' in range_str:
            start_page, end_page = map(int, range_str.split('-'))
            page_list.extend(range(start_page, end_page + 1))
        else:
            page_list.append(int(range_str))

    return sorted(page_list)


def extract_page_from_pdf(pdf_file_path, pages, output_file_path):
    # 打开PDF文件
    with open(pdf_file_path, 'rb') as pdf_file:
        # 创建一个PDF文件阅读器对象
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # 创建一个PDF文件写入器对象
        pdf_writer = PyPDF2.PdfWriter()

        # 遍历页面列表并提取页面
        for page_number in pages:
            try:
                page = pdf_reader.pages[page_number - 1] # 页面编号从1开始，所以需要减1
                pdf_writer.add_page(page)
            except IndexError:
                print(f"😱 页面编号 {page_number} 无效，PDF总页面数为 {len(pdf_reader.pages)}。")
                return

        # 打开输出文件
        with open(output_file_path, 'wb') as output_pdf:
            # 写入页面到输出文件
            pdf_writer.write(output_pdf)

        print(f"🎉 页面已成功提取到 {output_file_path}！")


""" Consts """
sub_dir_name = "extracted"  # 保存在子文件夹中。

# 目标文件路径：ctrl + shift + c
pdf_target = r"C:\Users\Havoc\Desktop\WHU's tasks\算法设计\课件\第九讲.pdf"
# WPS 的页面指定模式。
pages_choose = "4-8"


if __name__ == '__main__':
    # 文件夹路径
    sub_dir_path = os.path.join(os.path.dirname(pdf_target), sub_dir_name)
    if not os.path.exists(sub_dir_path):
        os.mkdir(sub_dir_path)

    # 解析页面字符串
    pages = parse_page_ranges(pages_choose)

    # TAG 提取页面
    extract_page_from_pdf(pdf_target, pages, os.path.join(sub_dir_path, os.path.basename(pdf_target)))
