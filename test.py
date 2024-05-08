import paddlehub as hub
import os
import cv2
import urllib
import numpy as np

order_no = "239s8gyfghda34"
url = 'https://pic5.40017.cn/i/ori/1kECr43w7yU.jpg'


resp = urllib.request.urlopen(url)
image = np.asarray(bytearray(resp.read()), dtype="uint8")
image = cv2.imdecode(image, cv2.IMREAD_COLOR)  # 将图片解码为cv2可以理解的格式

model_dir = os.getcwd() + '/modules/'
print(model_dir)

#ocr = hub.Module(directory = model_dir+'ch_pp_ocrv3')
ocr = hub.Module(directory="/Users/wangyi/Desktop/OCR/modules/ch_pp_ocrv3")
# ocr = hub.Module(name = 'ch_pp_ocrv3')
#

result = ocr.recognize_text(images=[image],)

print(result)