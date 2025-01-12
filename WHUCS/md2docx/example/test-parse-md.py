import mistune

# 创建一个 Markdown 解析器
md = mistune.create_markdown(renderer=None)

# 读取 Markdown 文件
with open("Python2Docx.md", 'r', encoding='utf-8') as md_file:
    markdown_content = md_file.read()

# 解析 Markdown
tokens, _ = md.parse(markdown_content)

# tokens 是一个包含文本和标记的列表
for tokens in tokens:
    print(tokens)
