from md5_handler.md5_handler import Md5HandlerAST
from docx_handler.docx_handler import DocxHandlerGenerator

class TransHandler:
    def __init__(self, file_path, base_file_path = None):
        self.tokens = None
        self.file_path = file_path
        self.base_file_path = base_file_path
        self.file_path_output = file_path.replace(".md", ".docx")

        self.md5 = Md5HandlerAST(file_path)
        self.docx = DocxHandlerGenerator()

    # def init(self):
    #     if self.base_file_path is not None:
    #         if self.base_file_path.endswith(".docx"):
    #             self.docx.load(self.base_file_path)
    #         else:
    #             self.docx.load_from_md(self.base_file_path)

    def trans(self, tokens=None):
        if tokens is None:
            tokens = self.md5.tokens
        for token in tokens:
            if token['type'] == 'heading':
                level = token['attrs']['level']
                title = token['children'][0]['raw']
                self.docx.add_title(self.md5.get_title(level), title, min(level, 2))
            elif token['type'] == 'blank_line':
                pass
            elif token['type'] == 'paragraph':
                self.trans(token['children'])
            elif token['type'] == 'text':
                self.docx.add_text(token['raw'])
            elif token['type'] == 'image':
                img_url = token['attrs']['url']
                text = token['children'][0]['raw']
                self.docx.add_picture_with_text( self.md5.get_img_num(), img_url, text)
            else:
                print(token)

    def save(self):
        try:
            self.docx.save(self.file_path_output)
            print("🐱 Saved!")
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            user_input = input("Do you want to try again? (y/n): ").strip().lower()
            if user_input == 'y':
                self.save()
            else:
                print("Operation cancelled.")
