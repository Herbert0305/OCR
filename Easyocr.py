# #EasyOCR是一个基于PyTorch的开源OCR库，可以进行多语言文本识别。它支持超过80种语言，不单单针对中文，但是账单识别准确率不高
# import easyocr
# # 加载预训练模型，这里是加载可同时识别简体中文和英文的对象，可根据自己需求指定其他语言的预训练模型
# reader = easyocr.Reader(['ch_sim', 'en'])
#
# img_path = '2.png'
# # 返回一个包含识别结果的列表
# result = reader.readtext(img_path, detail=0)
# # 处理识别结果
# results = '\n'.join(result)
# results = results.replace(' ', '')
# print(results)
import cv2
import numpy as np
import urllib.request

# 用 urllib.request.urlopen 读取图片内容
resp = urllib.request.urlopen('https://pic5.40017.cn/i/ori/1kECr43w7yU.jpg')
image = np.asarray(bytearray(resp.read()), dtype="uint8")
image = cv2.imdecode(image, cv2.IMREAD_COLOR)  # 将图片解码为cv2可以理解的格式
# 检查是否成功读取了图片
if image is not None:
    print("成功读取图片")
else:
    print("未读到图片，可能URL不正确或内容不是有效的图片数据")
# 显示处理后的图像
cv2.imshow('Processed Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
# 现在可以使用cv2.imshow展示图片，或者进行其他操作
# 例如 cv2.imshow('image',image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()