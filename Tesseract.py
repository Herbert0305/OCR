# from PIL import Image
# from pytesseract import pytesseract
#
# a = pytesseract.image_to_string(Image.open('2.png'), lang='chi_sim')
# print(a)
import cv2
import matplotlib.pyplot as plt

# 读取图像并转换为灰度图
image_path = 'shuiyin1.jpg'
image = cv2.imread(image_path)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 计算灰度直方图
histogram = cv2.calcHist([gray_image], [0], None, [256], [0, 256])

# 将直方图转换为占比
histogram_ratio = histogram / sum(histogram)
# 绘制灰度直方图
plt.figure(figsize=(10, 5))
plt.plot(histogram_ratio, color='gray')
plt.fill_between(range(256), histogram_ratio[:, 0], color='gray', alpha=0.5)
plt.title('Grayscale Histogram')
plt.xlabel('Grayscale Value')
plt.ylabel('Pixel Ratio')
plt.xlim([0, 255])
plt.show()