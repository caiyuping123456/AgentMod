def info(msg):
    """打印普通信息（蓝色标识）"""
    print(f"\033[34m[INFO] {msg}\033[0m")  # 蓝色字体

def error(msg):
    """打印错误信息（红色标识）"""
    print(f"\033[31m[ERROR] {msg}\033[0m")  # 红色字体

def warn(msg):
    """打印警告信息（黄色标识）"""
    print(f"\033[33m[WARN] {msg}\033[0m")   # 黄色字体