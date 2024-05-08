#https://blog.csdn.net/bugang4663/article/details/131687243?spm=1001.2014.3001.5501
from cnocr import CnOcr

def merge_texts_by_line(ocr_results, line_tolerance=10):
    lines = []
    ocr_results = sorted(ocr_results, key=lambda x: x['position'][0][1]) # 按照纵坐标排序

    current_line = []
    last_y0 = None

    for item in ocr_results:
        y0 = item['position'][0][1]
        if last_y0 is None or abs(y0 - last_y0) <= line_tolerance: # 在容差内视为同一行
            current_line.append(item['text'])
        else:
            if current_line:
                lines.append('～'.join(current_line)) # 合并当前行
            current_line = [item['text']] # 开始新的一行
        last_y0 = y0

    if current_line: # 确保最后一行也被添加
        lines.append('～'.join(current_line))

    return lines

# 示例用法:
img_path = '1.png'
ocr = CnOcr()
result = ocr.ocr(img_path)

# 提取文本和位置信息
#result 是一个列表，列表中的每个元素是一个字典，它包含了文本 (text)、得分 (score)，以及位置 (position) 信息
#访问字典的键，提取文本和位置信息
texts_with_positions = [
    {
        'text': item['text'],
        'position': item['position'].tolist()  # 将 numpy 数组转换为 Python 列表
    }
    for item in result
]

# 合并同一行的文本
merged_lines = merge_texts_by_line(texts_with_positions)

# 打印结果
for line in merged_lines:
    print(line)

# 具体参数设置参考：https://cnocr.readthedocs.io/zh/latest/usage/
