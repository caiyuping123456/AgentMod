import os.path
import yaml
import logging as log

# 读取yml文件
def read_yml(path:str)->str:
    if not os.path.exists(path):
        log.error("yml文件不存在")
        return None
    try:
        with open(path,'r',encoding='utf-8') as f:
            # 注意，读取到的是字典类型
            data = yaml.safe_load(f)
        log.info("成功读取到文件")
        return data
    except Exception as e:
        log.error("获取yml文件内容异常")
        return None