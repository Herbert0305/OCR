import cv2
import numpy as np

import cv2
import numpy as np

def enhance_text_visibility(image):

    # 转换到 YUV 颜色空间
    img_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)

    # 对亮度通道Y进行直方图均衡化
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])

    # 转换回 BGR 颜色空间
    image_equalized = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

    # 应用锐化滤波器
    kernel_sharpening = np.array([[-1,-1,-1],
                                  [-1, 9,-1],
                                  [-1,-1,-1]])
    sharpened = cv2.filter2D(image_equalized, -1, kernel_sharpening)
    return sharpened


def remove_watermark(image_path):
    # 读取图片
    image = cv2.imread(image_path)
    if image is None:
        print("Error loading image")
        return

    # 转换到HSV色彩空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 定义红色范围
    lower_red1 = np.array([0, 40, 50])  # 调整饱和度和亮度的下限
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([140, 40, 50])
    upper_red2 = np.array([180, 255, 255])

    # 创建掩模
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 | mask2

    # 膨胀和腐蚀
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)
    mask = cv2.erode(mask, kernel, iterations=1)

    # 使用不同的修复算法和参数尝试修复
    inpainted_image = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)


    # 水平堆叠原始图片和处理后的图片
    combined_image = np.hstack((image, inpainted_image))

    # 显示结果
    cv2.imshow('Original (Left) and Watermark Removed (Right)', combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



remove_watermark('red_shuiyin/shuiyin2.jpg')