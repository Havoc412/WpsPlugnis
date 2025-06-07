import mistune


class Md5HandlerAST:
    def __init__(self, file_path):
        self.tokens = None
        self.ast(file_path)

        self.title = [0] * 6  # 对应六级标题

        self.img_num = 0

    def ast(self, file_path):
        md = mistune.create_markdown(renderer=None)
        with open(file_path, 'r', encoding='utf-8') as md_file:
            markdown_content = md_file.read()

        self.tokens, _ = md.parse(markdown_content)

    def add_title(self, level):
        self.title[level-1] += 1
        for i in range(level, 6):
            self.title[i] = 0
        if level == 1:
            self.img_num = 0

    def get_title(self, level):
        self.add_title(level)
        for i, value in enumerate(self.title):
            if value == 0:
                return self.title[:i]
        return self.title

    def get_img_num(self):
        self.img_num += 1
        return [self.title[0], self.img_num]

if __name__ == '__main__':
    # md5_handler = Md5HandlerAST("../test/testdata/base.md")
    md5_handler = Md5HandlerAST("../../data/cloud/report-1.md")
    print(len(md5_handler.tokens))
    for token in md5_handler.tokens:
        print(token)