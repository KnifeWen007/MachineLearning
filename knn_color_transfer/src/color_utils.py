import numpy as np
import cv2
from skimage import color

def load_image(path):
    """
    加载图像 (默认使用 OpenCV 的 BGR 格式)。
    """
    import os
    # 检查文件是否存在
    if not os.path.exists(path):
        raise FileNotFoundError(f"图像文件不存在: {path} (当前工作目录: {os.getcwd()})")
    
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"无法加载图像: {path} (文件存在但OpenCV无法读取)")
    # OpenCV 默认是 BGR，我们转换为 RGB
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def save_image(img_rgb, path):
    """
    保存图像。
    """
    # 转换回 BGR 格式进行保存
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite(path, img_bgr)

def rgb_to_lab(img_rgb):
    """
    将 RGB 图像转换为 Lab 图像。
    skimage.color.rgb2lab 接受 [0, 255] 或 [0, 1] 的浮点数输入。
    """
    # 转换为 [0, 1] 范围的浮点数
    img_float = img_rgb.astype(np.float32) / 255.0
    # 使用 skimage 的 Lab 转换
    img_lab = color.rgb2lab(img_float)
    return img_lab

def lab_to_rgb(img_lab):
    """
    将 Lab 图像转换回 RGB 图像。
    """
    # 使用 skimage 的 RGB 转换
    img_float = color.lab2rgb(img_lab)
    # 转换回 [0, 255] 范围的整数
    img_rgb = (img_float * 255.0).clip(0, 255).astype(np.uint8)
    return img_rgb