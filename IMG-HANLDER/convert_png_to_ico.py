from PIL import Image
import os

def convert_png_to_ico(png_path, ico_path):
    """
    将 PNG 文件转换为 ICO 文件。
    
    :param png_path: 输入的 PNG 文件路径
    :param ico_path: 输出的 ICO 文件路径
    """
    try:
        # 打开 PNG 图像
        img = Image.open(png_path)
        
        # 转换为 ICO 格式并保存，指定更高的分辨率
        img.save(ico_path, format="ICO", sizes=[(256, 256)])
        
        print(f"成功将 {png_path} 转换为 {ico_path}")
    except Exception as e:
        print(f"转换失败: {e}")

if __name__ == "__main__":
    # 示例用法
    png_file = r"C:\Users\Havoc\Desktop\PS\Y1.png"
    ico_file = "example.ico"
    
    # 检查 PNG 文件是否存在
    if os.path.exists(png_file):
        convert_png_to_ico(png_file, ico_file)
    else:
        print(f"文件 {png_file} 不存在，请确保文件路径正确。")