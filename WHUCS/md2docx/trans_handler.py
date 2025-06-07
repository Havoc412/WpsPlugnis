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
                # 检查段落中是否有删除线文本
                has_strikethrough = False
                if 'children' in token:
                    for child in token['children']:
                        if child['type'] == 'text' and '~~' in child['raw']:
                            has_strikethrough = True
                            break
                
                # 打印段落内容，用于调试
                if has_strikethrough:
                    print("发现包含删除线的段落:")
                    print(token)
                
                self.docx.add_paragraph_with_runs(token['children'])
            elif token['type'] == 'text':
                # 处理可能包含删除线的单独文本
                text = token['raw']
                if '~~' in text:
                    # 使用自定义方法处理带删除线的文本
                    self.docx.add_text_with_strikethrough(text)
                else:
                    self.docx.add_text(text)
            elif token['type'] == 'image':
                img_url = token['attrs']['url']
                text = token['children'][0]['raw']
                self.docx.add_picture_with_text(self.md5.get_img_num(), img_url, text)
            elif token['type'] == 'strong':
                self.docx.add_bold_text(token['children'][0]['raw'])
            elif token['type'] == 'em':
                self.docx.add_italic_text(token['children'][0]['raw'])
            elif token['type'] == 's':
                self.docx.add_strikethrough_text(token['children'][0]['raw'])
            elif token['type'] == 'code':
                self.docx.add_inline_code(token['raw'])
            elif token['type'] == 'code_block':
                self.docx.add_code_block(token['raw'], token['attrs'].get('info', ''))
            elif token['type'] == 'blockquote':
                self.docx.add_quote(token['children'])
            elif token['type'] == 'bullet_list':
                self.docx.add_bullet_list(token['children'])
            elif token['type'] == 'ordered_list':
                self.docx.add_ordered_list(token['children'])
            elif token['type'] == 'list_item':
                self.trans(token['children'])
            elif token['type'] == 'table':
                self.docx.add_table(token['children'])
            elif token['type'] == 'thematic_break':
                self.docx.add_horizontal_rule()
            elif token['type'] == 'footnote':
                self.docx.add_footnote(token['children'][0]['raw'])
            elif token['type'] == 'math':
                self.docx.add_math(token['raw'], is_inline=token['attrs'].get('inline', False))
            elif token['type'] == 'emphasis':
                if 'children' in token and token['children']:
                    child = token['children'][0]
                    if 'raw' in child:
                        self.docx.add_italic_text(child['raw'])
                    elif 'children' in child:
                        self.trans(child['children'])
            elif token['type'] == 'codespan':
                if 'raw' in token:
                    self.docx.add_inline_code(token['raw'])
            elif token['type'] == 'list':
                if 'children' in token:
                    if token['attrs'].get('ordered', False):
                        self.docx.add_ordered_list(token['children'])
                    else:
                        self.docx.add_bullet_list(token['children'])
            elif token['type'] == 'block_quote':
                if 'children' in token:
                    self.docx.add_quote(token['children'])
            elif token['type'] == 'block_code':
                if 'raw' in token:
                    self.docx.add_code_block(token['raw'], token['attrs'].get('info', ''))
            elif token['type'] == 'softbreak':
                self.docx.add_text('\n')
            elif token['type'] == 'link':
                if 'children' in token and token['children'] and 'attrs' in token:
                    text = token['children'][0].get('raw', '')
                    url = token['attrs'].get('url', '')
                    self.docx.add_hyperlink(text, url)
            else:
                print(f"Unhandled token type: {token['type']}")

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
