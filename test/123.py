import os
import shutil
import glob
import random

# --- 配置您的目录路径和划分比例 ---
# 1. 图片和标签的根目录
BASE_DIR = r'D:\Py_Project\Langcahin\test'

# 2. 原始图片和标签的目录
# 2. 原始图片和标签的目录
# ❗ 修正：只提供相对于 BASE_DIR 的目录名 'img' 和 'out'
IMAGE_SOURCE_DIR = os.path.join(BASE_DIR, 'img')  # 您的图片在 D:\...\test\img
LABEL_SOURCE_DIR = os.path.join(BASE_DIR, 'out')  # 您的标签在 D:\...\test\out

# 3. 目标数据集结构根目录 (例如 'test/a')
# ❗ 修正：只提供相对于 BASE_DIR 的目录名 'a'
TARGET_ROOT_DIR = os.path.join(BASE_DIR, 'a')

# 4. 划分比例 (80% 训练集, 20% 验证集)
TRAIN_RATIO = 0.8
VAL_RATIO = 0.2

# --- 目标目录的完整路径 ---
# 图片目标目录
TRAIN_IMG_DIR = os.path.join(TARGET_ROOT_DIR, 'images', 'train')
VAL_IMG_DIR = os.path.join(TARGET_ROOT_DIR, 'images', 'val')
# 标签目标目录
TRAIN_LABEL_DIR = os.path.join(TARGET_ROOT_DIR, 'labels', 'train')
VAL_LABEL_DIR = os.path.join(TARGET_ROOT_DIR, 'labels', 'val')


def create_directories():
    """创建所有目标目录。"""
    print("--- 1. 检查并创建目标目录 ---")

    # 需要创建的目录列表
    dirs_to_create = [
        TRAIN_IMG_DIR, VAL_IMG_DIR,
        TRAIN_LABEL_DIR, VAL_LABEL_DIR
    ]

    for directory in dirs_to_create:
        os.makedirs(directory, exist_ok=True)
        print(f"Directory created/exists: {directory}")
    print("-" * 30)


def split_and_move_files():
    """执行文件划分和移动操作。"""
    print("--- 2. 获取文件列表 ---")

    # 获取所有图片文件的完整路径
    # 假设图片是 .jpg 格式，如果您的图片是 .png, .jpeg 等，请修改 glob 模式
    image_paths = glob.glob(os.path.join(IMAGE_SOURCE_DIR, '*.*'))

    if not image_paths:
        print(f"Error: No image files found in {IMAGE_SOURCE_DIR}. Please check the path and file extensions.")
        return

    # 提取所有图片的文件名（不含扩展名），作为划分的依据
    all_files = [os.path.splitext(os.path.basename(p))[0] for p in image_paths]

    # 随机打乱文件列表
    random.shuffle(all_files)
    total_files = len(all_files)
    print(f"Found {total_files} file pairs (images + labels) to process.")

    # 计算划分索引
    train_split_index = int(total_files * TRAIN_RATIO)

    # 划分数据集
    train_files = all_files[:train_split_index]
    val_files = all_files[train_split_index:]

    print(f"Training set size: {len(train_files)} files.")
    print(f"Validation set size: {len(val_files)} files.")
    print("-" * 30)

    # 3. 移动文件到目标目录
    def move_pair(file_name, img_target_dir, label_target_dir):
        """移动单个图片和对应的标签文件。"""
        # 查找图片文件 (使用 glob 避免硬编码图片后缀)
        img_match = glob.glob(os.path.join(IMAGE_SOURCE_DIR, f"{file_name}.*"))
        if not img_match:
            print(f"Warning: Image for {file_name} not found. Skipping.")
            return

        # 查找标签文件 (标签后缀固定为 .txt)
        label_source_path = os.path.join(LABEL_SOURCE_DIR, f"{file_name}.txt")
        if not os.path.exists(label_source_path):
            print(f"Warning: Label TXT for {file_name} not found. Skipping.")
            return

        # 移动图片
        img_source_path = img_match[0]
        img_target_path = os.path.join(img_target_dir, os.path.basename(img_source_path))
        shutil.copy(img_source_path, img_target_path)

        # 移动标签
        label_target_path = os.path.join(label_target_dir, os.path.basename(label_source_path))
        shutil.copy(label_source_path, label_target_path)

    print("--- 3. 移动文件 ---")
    # 移动训练集文件
    print("Moving Training Files...")
    for file_name in train_files:
        move_pair(file_name, TRAIN_IMG_DIR, TRAIN_LABEL_DIR)

    # 移动验证集文件
    print("Moving Validation Files...")
    for file_name in val_files:
        move_pair(file_name, VAL_IMG_DIR, VAL_LABEL_DIR)

    print("-" * 30)
    print("All files have been successfully split and moved/copied.")
    print(f"Your YOLO dataset is ready in {TARGET_ROOT_DIR}")


# --- 主执行逻辑 ---
if __name__ == "__main__":
    create_directories()
    split_and_move_files()