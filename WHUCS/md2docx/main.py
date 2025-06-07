import os
from idlelib.pyparse import trans

from trans_handler import TransHandler

def check_file_path(file_path):
    if not os.path.exists(file_path):
        print("File path does not exist")
        exit(1)

    docx_file_path = file_path.replace(".md", ".docx")
    if os.path.exists(docx_file_path):
        user_input = input("❗Docx file already exists. Do you want to replace it? (y/n): ").strip().lower()
        if user_input != 'y':
            print("Operation cancelled.")
            exit(1)


MD_FILE_PATH = r"../data/cloud/report-1.md"
# MD_FILE_PATH = r"./test/testdata/base.md"
BASE_DOCX_FILE_PATH = None


if __name__ == '__main__':
    # 1. check file path
    check_file_path(MD_FILE_PATH)
    if BASE_DOCX_FILE_PATH is not None:
        check_file_path(BASE_DOCX_FILE_PATH)
    # 2. run
    trans_handler = TransHandler(MD_FILE_PATH, BASE_DOCX_FILE_PATH)

    trans_handler.trans()
    trans_handler.save()

