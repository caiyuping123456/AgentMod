import xml.etree.ElementTree as ET
import os
import glob

# --- 配置您的目录和类别信息 ---
# 1. 您的 XML 文件所在目录（对应您图中的 'data'）
XML_INPUT_DIR = r'D:\Py_Project\Langcahin\test\data'

# 2. TXT 标签文件输出目录（对应您图中的 'out'）
TXT_OUTPUT_DIR = r'D:\Py_Project\Langcahin\test\out'

# 3. 类别名称到 YOLO 整数索引的映射
# ！！！请务必根据您的XML文件内容和数据集定义来设置！！！
# 假设您的数据集中只有 'fire' 这一类，且索引为 0。
CLASS_TO_INDEX = {
    'fire': 0,
    # 如果有其他类别，例如：
    # 'smoke': 1,
    # 'person': 2,
}


# --- 转换函数 ---
def convert_xml_to_yolo_txt(xml_path, output_dir, class_map):
    """
    将单个 Pascal VOC 格式的 XML 文件转换为 YOLO 格式的 TXT 文件。
    """
    try:
        # 1. 解析 XML
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # 提取图像尺寸 (width, height)
        size_elem = root.find('size')
        if size_elem is None:
            print(f"Error: <size> tag missing in {xml_path}. Skipping.")
            return

        img_width = int(size_elem.find('width').text)
        img_height = int(size_elem.find('height').text)

        # 确定输出 TXT 文件路径
        filename = root.find('filename').text
        # 使用 XML 文件名作为基础，确保和图片名称一致
        base_name = os.path.splitext(os.path.basename(xml_path))[0]
        txt_path = os.path.join(output_dir, base_name + '.txt')

        yolo_lines = []

        # 遍历所有 <object> 标签
        for obj in root.findall('object'):
            class_name = obj.find('name').text

            # 2. 类别映射
            if class_name not in class_map:
                print(f"Warning: Class '{class_name}' not in map. Skipping object in {xml_path}.")
                continue
            class_index = class_map[class_name]

            bndbox = obj.find('bndbox')
            if bndbox is None: continue  # 避免没有边界框

            # 提取边界框坐标 (xmin, ymin, xmax, ymax)
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)

            # 3. 计算归一化坐标
            # 边界框中心点坐标
            x_center = (xmin + xmax) / 2.0
            y_center = (ymin + ymax) / 2.0

            # 边界框宽度和高度
            bbox_width = xmax - xmin
            bbox_height = ymax - ymin

            # 归一化 (除以图像尺寸)
            x_center_norm = x_center / img_width
            y_center_norm = y_center / img_height
            width_norm = bbox_width / img_width
            height_norm = bbox_height / img_height

            # 格式化为 YOLO 格式的行 (class_index x_center y_center width height)
            line = f"{class_index} {x_center_norm:.6f} {y_center_norm:.6f} {width_norm:.6f} {height_norm:.6f}"
            yolo_lines.append(line)

        # 4. 写入 TXT
        with open(txt_path, 'w') as f:
            f.write('\n'.join(yolo_lines))

        print(f"Converted {os.path.basename(xml_path)} -> {os.path.basename(txt_path)}")

    except Exception as e:
        print(f"Failed to process {xml_path}. Error: {e}")


# --- 主执行逻辑 ---
if __name__ == "__main__":
    # 确保输出目录存在
    os.makedirs(TXT_OUTPUT_DIR, exist_ok=True)

    # 获取输入目录下所有的 .xml 文件路径
    xml_files = glob.glob(os.path.join(XML_INPUT_DIR, '*.xml'))

    if not xml_files:
        print(f"No XML files found in the directory: {XML_INPUT_DIR}")
    else:
        print(f"Found {len(xml_files)} XML files. Starting conversion...")
        for xml_file in xml_files:
            convert_xml_to_yolo_txt(xml_file, TXT_OUTPUT_DIR, CLASS_TO_INDEX)

        print("\n--- Conversion Complete ---")