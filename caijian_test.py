import cv2
import numpy as np

import numpy as np
import cv2
import os

def should_process_image(image, width_height_ratio_threshold=1):
    """
    检查图片的宽高比是否小于设定的阈值。

    :param image_path: 图片的路径。
    :param width_height_ratio_threshold: 宽高比的最大阈值，超过这个值的图片认为是电脑截图。
    :return: 如果图片的宽高比小于阈值，返回 True，否则返回 False。
    """
    height, width = image.shape[:2]
    # 计算宽高比
    width_height_ratio = width / height
    print(f"width_height_ratio: {width_height_ratio}")
    return width_height_ratio <= width_height_ratio_threshold

def crop_black_borders(image, gray_image, low_threshold, high_threshold, black_proportion_threshold):
    # 计算低于low_threshold的像素的比例
    black_pixels = np.sum(gray_image < low_threshold)
    total_pixels = gray_image.size
    black_proportion = black_pixels / total_pixels
    print(black_proportion)
    # 如果黑色部分超过了阈值比例，则裁剪图像
    if black_proportion > black_proportion_threshold:
        print("黑色裁剪")
        # 找到非黑色的行
        rows_not_black = np.where(np.mean(gray_image, axis=1) > high_threshold)[0]
        if len(rows_not_black) > 0:
            top_row = rows_not_black[0]
            bottom_row = rows_not_black[-1]
            cropped_image = image[top_row:bottom_row, :]
            return cropped_image
        else:
            print("不裁剪")
            return image  # 如果所有行都是黑色的，则不裁剪
    else:
        print("不需要黑色裁剪")
        return image  # 如果黑色部分没有超过阈值比例，则不裁剪


def crop_white_borders(image, gray_image, high_threshold, white_proportion_threshold):
    # 计算高于high_threshold的白色像素的比例
    white_pixels = np.sum(gray_image > high_threshold)
    total_pixels = gray_image.size
    white_proportion = white_pixels / total_pixels
    print(white_proportion)

    # 如果白色部分超过了阈值比例，则裁剪图像
    if white_proportion > white_proportion_threshold:
        print("白色裁剪")
        # 找到非白色的行
        rows_not_white = np.where(np.mean(gray_image, axis=1) < high_threshold)[0]
        if len(rows_not_white) > 0:
            top_row = rows_not_white[0]
            bottom_row = rows_not_white[-1]
            cropped_image = image[top_row:bottom_row + 1, :]
            if should_process_image(cropped_image, 1.2):  # 我们设置的阈值是1.2
                # 图片的宽高比小于或等于1.5，处理这张图片
                print(f"图片的宽高比小于或等于1.2，返回原图")
                return image
            else:
                # 图片的宽高比大于1.5，跳过这张图片
                print(f"图片的宽高比大于1.2，坏图，跳过")
                return cropped_image
        else:
            print("不裁剪")
            return image  # 如果所有行都是白色的，则不裁剪
    else:
        print("不需要裁剪")
        return image  # 如果白色部分没有超过阈值比例，则不裁剪


# 示例使用：
# image: 输入的RGB图像
# gray_image: 输入图像的灰度版本
# high_threshold: 用于判断白色像素的阈值
# white_proportion_threshold: 裁剪的阈值比例

# 读取图像并转换为灰度图
img = cv2.imread('bai_cai.png')
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 设置黑色的阈值
low_threshold = 5  # 低于此值被认为是黑色
high_threshold = 50  # 用于确定非黑色行的阈值，可能需要根据图像调整
black_proportion_threshold = 0.1  # 黑色像素占图像的10%
high_threshold_bai = 236    #初始：236
white_proportion_threshold = 0.2
# 裁剪图像
processed_img = crop_black_borders(img, gray_img, low_threshold, high_threshold, black_proportion_threshold)

img2 = crop_white_borders(processed_img, gray_img, high_threshold_bai, white_proportion_threshold)
# 显示处理后的图像
cv2.imshow('Processed Image', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()