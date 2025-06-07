import os
import PyPDF2


def merge_pdfs(directory):
    # 获取指定目录下的所有PDF文件
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]

    # 创建一个PDF文件写入器
    pdf_writer = PyPDF2.PdfWriter()

    # 遍历PDF文件并添加到写入器
    for pdf_file in pdf_files:
        pdf_path = os.path.join(directory, pdf_file)
        pdf_reader = PyPDF2.PdfReader(pdf_path)

        # 添加每一页到PDF写入器
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])

    # 输出合并后的PDF文件
    merged_pdf_path = os.path.join(directory, 'merged.pdf')
    with open(merged_pdf_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

    print(f'Merged PDF saved as {merged_pdf_path}')


# 指定文件夹路径
folder_path = r"../data"

# 调用函数合并PDF
merge_pdfs(folder_path)
