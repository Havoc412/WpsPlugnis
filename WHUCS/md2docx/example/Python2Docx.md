# 尝试：直接用 python 处理 word

参考：<https://blog.csdn.net/qq_41314882/article/details/134922594>

由于有的课程还是必须提交 word 版本，所以还是这样尝试一下。

主要处理的就是：

1.  各级标题、正文
2.  图片图例
3.  目录生成？（或许可以直接依靠 WPS）

# 参考教程-2

URL：<https://blog.csdn.net/lly1122334/article/details/109669667>

基本的效果如下，解析 md5 转换到实验要求的 docx 看起来也不是很难的事情了，主要就是设置好基本的 “模板”。

ps. 做的过程中同时也思考一下**可扩展性**的。

![屏幕截图 2024-12-21 061800.png](https://www.helloimg.com/i/2024/12/21/6765ed167c8f8.png)

# 函数 Pre

## 图例处理

### bug：opencv2 对中文路由的异常

![屏幕截图 2024-12-21 225705.png](https://www.helloimg.com/i/2024/12/21/6766d73c78a90.png)

想起来了，之前也遇到过这个问题。

#### solved：

参考：<https://blog.csdn.net/wenqiwenqi123/article/details/122258804>

> 很多小伙伴在使用python的opencv（cv2）的时候，肯定都碰到过读取中文路径的图片失败的问题。因为直接使用 cv2.imread(filename)并不支持中文路径。
>
> 这边直接给出用cv2能够读取和保存中文路径图片的python代码：

```python
def test():
    pass
```































