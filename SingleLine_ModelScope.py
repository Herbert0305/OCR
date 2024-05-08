#https://modelscope.cn/models/iic/cv_convnextTiny_ocr-recognition-general_damo/summary
# from modelscope.pipelines import pipeline
# from modelscope.utils.constant import Tasks
#
# ocr_recognition = pipeline(Tasks.ocr_recognition, model='damo/cv_convnextTiny_ocr-recognition-general_damo')
#
# ### 使用url
# img_url = '2.png'
# result = ocr_recognition(img_url)
# print(result)

### 使用图像文件
### 请准备好名为'ocr_recognition.jpg'的图像文件
# img_path = 'ocr_recognition.jpg'
# img = cv2.imread(img_path)
# result = ocr_recognition(img)
# print(result)

# 导入必要的库
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as mbox
from PIL import ImageTk, Image
import cv2
#
# # 主窗口配置
# window = tk.Tk()  # 创建一个tkinter GUI窗口框架
# window.title("图片水印移除")  # 窗口标题
# window.geometry('1000x700')  # 窗口大小
#
# # 顶部标签
# start1 = tk.Label(text="图片水印移除", font=("Arial", 50), fg="magenta")  # 设置字体和颜色
# start1.place(x=80, y=10)
#
# # 移除水印的函数
# def remove_watermark():
#     # 打开文件对话框选择图片文件
#     img_path = "shuiyin2.jpg"
#
#     # 读取图片文件
#     img = cv2.imread(img_path, 1)
#
#     # 处理图片以移除水印
#     _, thresh = cv2.threshold(img, 170, 255, cv2.THRESH_BINARY)
#
#     # 显示移除水印后的图片
#     cv2.imshow('去除水印后的图片', thresh)
#
#     # 等待按键然后销毁所有窗口
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
# remove_watermark()

import cv2
import os

def should_process_image(image_path, width_height_ratio_threshold=1):
    """
    检查图片的宽高比是否小于设定的阈值。

    :param image_path: 图片的路径。
    :param width_height_ratio_threshold: 宽高比的最大阈值，超过这个值的图片认为是电脑截图。
    :return: 如果图片的宽高比小于阈值，返回 True，否则返回 False。
    """
    image = cv2.imread(image_path)
    if image is None:
        return False
    height, width = image.shape[:2]
    # 计算宽高比
    width_height_ratio = width / height
    print(width_height_ratio)
    return width_height_ratio <= width_height_ratio_threshold

# 用法示例
image_folder_path = 'image'
for img_file in os.listdir(image_folder_path):
    img_path = os.path.join(image_folder_path, img_file)
    if img_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif')):
        if should_process_image(img_path, 1.2):  # 假设我们设置的阈值是1.5
            # 图片的宽高比小于或等于1.5，处理这张图片
            print(f"Processing image: {img_path}")
        else:
            # 图片的宽高比大于1.5，跳过这张图片
            print(f"Skipping wide image: {img_path}")