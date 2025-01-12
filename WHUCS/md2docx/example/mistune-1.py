import mistune

markdown_text = "# Hello World\n这是一个 Markdown 文档。\n- 列表项1\n- 列表项2\n**加粗文本**"

# TIP 取消 render，直接操作 AST。
markdown = mistune.create_markdown(renderer=None)
tokens = markdown.parse(markdown_text)

# 打印每个 Token 的信息
print(len(tokens))
for token in tokens[0]:  # 拿到的第二个数值有些奇怪。
    print(token)
