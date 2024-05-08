import paddlehub as hub
import paddle
import cv2
import os
import numpy as np

a = 0
num = {}
#判断黑色裁剪函数
def crop_black_borders(image, gray_image, low_threshold, high_threshold, black_proportion_threshold):
    # 计算低于low_threshold的像素的比例
    black_pixels = np.sum(gray_image < low_threshold)
    total_pixels = gray_image.size
    black_proportion = black_pixels / total_pixels
    #print(black_proportion)
    # 如果黑色部分超过了阈值比例，则裁剪图像
    if black_proportion > black_proportion_threshold:
        print("白色裁剪")
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
#判断白色裁剪
def crop_white_borders(image, gray_image, high_threshold, white_proportion_threshold):
    # 计算高于high_threshold的白色像素的比例
    white_pixels = np.sum(gray_image > high_threshold)
    total_pixels = gray_image.size
    white_proportion = white_pixels / total_pixels
    # print(white_proportion)

    # 如果白色部分超过了阈值比例，则裁剪图像
    if white_proportion > white_proportion_threshold:
        print("白色裁剪")
        # 找到非白色的行
        rows_not_white = np.where(np.mean(gray_image, axis=1) < high_threshold)[0]
        if len(rows_not_white) > 0:
            top_row = rows_not_white[0]
            bottom_row = rows_not_white[-1]
            cropped_image = image[top_row:bottom_row + 1, :]
            return cropped_image
        else:
            print("不裁剪")
            return image  # 如果所有行都是白色的，则不裁剪
    else:
        print("不需要白色裁剪")
        return image  # 如果白色部分没有超过阈值比例，则不裁剪

# 定义一个函数，用于格式化输出合并后的行
def print_merged_lines(lines):
    for line in lines:
        merged_text = " ~ ".join(line.split())  # 使用 ~ 作为分隔符
        print(merged_text)

# 更新后的遮挡检测函数，增加了亮点检测
def detect_obstructions(image, bright_threshold=260, dark_threshold=160, obstruction_threshold=0.30, bright_spot_area_threshold=500, circularity_threshold=0.75):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用阈值方法来检测过亮或过暗的区域
    _, bright_areas = cv2.threshold(gray, bright_threshold, 255, cv2.THRESH_BINARY)
    _, dark_areas = cv2.threshold(gray, dark_threshold, 255, cv2.THRESH_BINARY_INV)
    # 检测亮点
    contours, _ = cv2.findContours(bright_areas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        circularity = 4 * np.pi * (area / (perimeter * perimeter + 1e-10))
        if area > bright_spot_area_threshold and circularity > circularity_threshold:
            return True  # 检测到亮点，返回True表示存在遮挡

    # 检测亮暗区域的面积占比
    bright_area_ratio = cv2.countNonZero(bright_areas) / (image.shape[0] * image.shape[1])
    dark_area_ratio = cv2.countNonZero(dark_areas) / (image.shape[0] * image.shape[1])
    print(bright_area_ratio)
    print(dark_area_ratio)
    num[a] = dark_area_ratio

    # 设定亮暗区域的面积占比阈值
    return bright_area_ratio > obstruction_threshold or dark_area_ratio > obstruction_threshold


# 自适应阈值处理增强文字对比度
# 移除水印的函数
def remove_watermark(img):
    # 处理图片以移除水印，应用阈值
    _, thresh = cv2.threshold(img, 170, 255, cv2.THRESH_BINARY)

    # 返回去除水印后的图片
    return thresh

# 定义一个函数，用于合并同一行的文本
def merge_lines(data, y_threshold=10):
    # 根据文本框的上边界y坐标进行排序
    # sorted_data = sorted(data, key=lambda x: min([pos[1] for pos in x['text_box_position']]))
    sorted_data = data
    lines = []
    current_line = []
    current_y = None

    for item in sorted_data:
        text_box_position = item['text_box_position']
        # 计算文本框的平均y坐标
        avg_y = sum([pos[1] for pos in text_box_position]) / 4
        # 如果当前行为空或者文本框的y坐标接近当前行的y坐标，则合并到当前行
        if current_y is None or abs(avg_y - current_y) < y_threshold:
            current_line.append(item['text'])
            current_y = avg_y
        else:
            lines.append(' '.join(current_line))
            current_line = [item['text']]
            current_y = avg_y
    # 添加最后一行
    if current_line:
        lines.append(' '.join(current_line))
    return lines

# 检查文本中是否包含关键词
def check_keywords(lines, keywords):
    for line in lines:
        for keyword in keywords:
            if keyword in line:
                return True
    return False
# 加载OCR模型
#ocr = hub.Module(name="ch_pp-ocrv3")
# 定义一个关键词列表
keywords = ["交易时间", "汇款日期", "付款银行", "收款人", "付款人", "收款方", "汇款人姓名"]

# # 定义图片文件夹路径:文件夹处理
# image_folder_path = 'image'
#
# # 遍历image文件夹中的所有图片
# for img_file in os.listdir(image_folder_path):
#     img_path = os.path.join(image_folder_path, img_file)
#     if img_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif')):
#         image = cv2.imread(img_path)
#         print(f"处理文件: {img_path}")
#         gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#         # # 去除水印
#         # image_no_watermark = remove_background_watermark(image)
#
#         # 裁剪图像
#         # 参数：low_threshold = 5，high_threshold = 50，black_proportion_threshold = 0.1
#         cropped_image=crop_black_borders(image, gray_image, 5, 50, 0.1)
#         cropped_image2 = crop_white_borders(cropped_image, gray_image, 236, 0.2)
#         # 使用遮挡检测
#         if detect_obstructions(cropped_image2):
#             print(f"图片质量不佳，存在明显的遮挡: {img_path}")
#             continue  # 继续处理下一张图片
#         a = a+1
#         # 使用OCR进行文字识别
#         result = ocr.recognize_text(images=[cropped_image])
#
#         if result is not None and len(result) > 0:
#             ocr_data = result[0]['data']
#             lines = merge_lines(ocr_data)
#             if check_keywords(lines, keywords):
#
#                 #continue
#                 #print(f"这张图符合规范的: {img_path}")
#                 ocr_data = result[0]['data']  # 获取OCR识别的数据
#                 lines = merge_lines(ocr_data)  # 合并同一行的文本
#                 #print(lines)      # 打印合并后的行
#             else:
#                 print(f"图片不符合规范: {img_path}")
#         else:
#             print("No text detected in the image.")
# for i in num:
#     print(num[i])
#单张：14:0.335 ,63:0.74,3:0.381    33:0.17   zhedang:0.172  shuiyin1:0.24
img_path = 'qian.png'

image = cv2.imread(img_path)
#裁剪图像
# 参数：low_threshold = 5，high_threshold = 50，black_proportion_threshold = 0.1
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 去除水印
image_no_watermark = remove_watermark(image)
# # 显示移除水印后的图片
# cv2.imshow('去除水印后的图片', image_no_watermark)
#
# # 等待按键然后销毁所有窗口
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# 裁剪图像
cropped_image =crop_black_borders(image, gray_image, 5, 50, 0.1)
cropped_image2 = crop_white_borders(cropped_image,gray_image,236,0.1)
# 在OCR检测前先使用遮挡检测
if detect_obstructions(cropped_image2):
    print("图片有遮挡")

else:
    image_no_watermark = remove_watermark(cropped_image)
    # 加载OCR模型
    model_dir = os.getcwd() + '/modules/'
    print(model_dir)
    # ocr = hub.Module(directory=model_dir + 'ch_pp_ocrv3')
    ocr = hub.Module(directory="/Users/wangyi/Desktop/OCR/modules/ch_pp_ocrv3")
    #ocr = paddle.jit.load("/ch_pp_ocrv3/inference_model/ppocrv3_rec.pdmodel")
    # 使用OCR对图片进行文字识别
    result = ocr.recognize_text(images=[image_no_watermark])

    # 检查是否有识别结果
    if result is not None and len(result) > 0:
        ocr_data = result[0]['data']  # 获取OCR识别的数据
        lines = merge_lines(ocr_data)  # 合并同一行的文本

        # 定义一个关键词列表
        keywords = ["交易时间", "汇款日期", "付款银行", "收款人", "付款人", "收款方","付款方户名","付款方账号","收款方账号"]

        # 检查是否有关键词
        if check_keywords(lines, keywords):
            print("这张图是有用的，进行后续操作。")
            # 检查是否有识别结果
            if result is not None and len(result) > 0:
                ocr_data = result[0]['data']  # 获取OCR识别的数据
                print(ocr_data)
                lines = merge_lines(ocr_data)  # 合并同一行的文本
                print_merged_lines(lines)      # 打印合并后的行
        else:
            print("图片不含关键词。")
    else:
        print("No text detected.")