import paddlehub as hub
import cv2

# 定义一个函数，用于合并同一行的文本
def merge_lines(data, y_threshold=12):
    # 根据文本框的上边界y坐标进行排序
    sorted_data = sorted(data, key=lambda x: min([pos[1] for pos in x['text_box_position']]))
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

#处理关键词数据
def extract_valid_data(lines, valid_keywords):
    extracted_data = {keyword: "" for keyword in valid_keywords}
    # 对每行数据进行处理
    for line in lines:
        # 移除行两边的空白，并分割行来提取可能的关键词和值
        parts = line.strip().split()
        for part in parts:
            if part in valid_keywords:
                # 根据关键词位置，提取值
                keyword_index = parts.index(part)
                # 如果关键词在行首，值在其后
                if keyword_index == 0 and len(parts) > 1:
                    value = " ".join(parts[1:])
                # 如果关键词在行尾，值在其前
                elif keyword_index == len(parts) - 1 and len(parts) > 1:
                    value = " ".join(parts[:-1])
                # 如果关键词和值在同一个位置（即行中只有一个词），则跳过
                else:
                    continue
                extracted_data[part] = value
                break  # 找到关键词，跳出循环
    return extracted_data

# 定义一个函数，用于格式化输出提取后的数据
def print_extracted_data(extracted_data, valid_keywords):
    for keyword in valid_keywords:
        # 检查关键词是否有匹配的数据行
        if extracted_data[keyword]:
            print(f"{keyword} ~ {extracted_data[keyword]}")


img_path = '2.png'

# 加载OCR模型
ocr = hub.Module(name="ch_pp-ocrv3")

# 使用OCR对图片进行文字识别
result = ocr.recognize_text(images=[cv2.imread(img_path)])
print(result)
#定义有效的关键词列表
valid_keywords = [
    "交易时间","交易卡号","业务摘要","交易场所","交易金额","交易类型",
    "记账金额","转账金额","大写金额","记账币种","交易卡余额",
    "对方账户","对方户名","凭证号","户名","对方账户行别","账户","收款银行",
]

# 检查是否有识别结果
if result is not None and len(result) > 0:
    ocr_data = result[0]['data']  # 获取OCR识别的数据
    lines = merge_lines(ocr_data)  # 合并同一行的文本
    extracted_data = extract_valid_data(lines, valid_keywords)  # 提取有效数据
    print_extracted_data(extracted_data, valid_keywords)  # 打印提取后的数据
else:
    print("No text detected.")