# import paddlehub as hub
# import cv2
#
# # 定义一个函数，用于合并同一行的文本
# def merge_lines(data, y_threshold=10):
#     # 根据文本框的上边界y坐标进行排序
#     sorted_data = sorted(data, key=lambda x: min([pos[1] for pos in x['text_box_position']]))
#     lines = []
#     current_line = []
#     current_y = None
#
#     for item in sorted_data:
#         text_box_position = item['text_box_position']
#         # 计算文本框的平均y坐标
#         avg_y = sum([pos[1] for pos in text_box_position]) / 4
#
#         # 如果当前行为空或者文本框的y坐标接近当前行的y坐标，则合并到当前行
#         if current_y is None or abs(avg_y - current_y) < y_threshold:
#             current_line.append(item['text'])
#             current_y = avg_y
#         else:
#             lines.append(' '.join(current_line))
#             current_line = [item['text']]
#             current_y = avg_y
#
#     # 添加最后一行
#     if current_line:
#         lines.append(' '.join(current_line))
#
#     return lines
#
# # 定义一个函数，用于格式化输出合并后的行
# def print_merged_lines(lines):
#     for line in lines:
#         merged_text = " ~ ".join(line.split())  # 使用 ~ 作为分隔符
#         print(merged_text)
#
# img_path = 'image/2.jpeg'
#
# # 加载OCR模型
# ocr = hub.Module(name="ch_pp-ocrv3")
#
# # 使用OCR对图片进行文字识别
# result = ocr.recognize_text(images=[cv2.imread(img_path)])
#
# # 检查是否有识别结果
# if result is not None and len(result) > 0:
#     ocr_data = result[0]['data']  # 获取OCR识别的数据
#     lines = merge_lines(ocr_data)  # 合并同一行的文本
#     print_merged_lines(lines)      # 打印合并后的行
# else:
#     print("No text detected.")