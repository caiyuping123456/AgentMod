import os

from langchain_core.tools import tool
from pydantic import BaseModel, Field


class FieldInfo(BaseModel):
    doc_path:str = Field(description="文件或目录的具体路径。可以是绝对路径（如 '/home/user/data.txt'）或相对于当前工作目录的路径。")

# 判断文件是否存在
# doc_path表示文件的具体路径
@tool(
    name_or_callable="parser_doc_content",
    description= "用于检查文件/目录是否存在，并根据类型执行不同操作：\n"
        "1. 如果是文件：读取并返回其完整文本内容（自动处理 utf-8/gbk 编码）。\n"
        "2. 如果是目录：递归遍历该目录及其子目录，返回找到的所有文件路径列表。\n"
        "3. 如果路径不存在或为空：返回具体的错误信息。\n"
        "注意：对于大型目录，可能只返回部分文件列表以防输出过长。",
    args_schema=FieldInfo,
    return_direct=False
)
def parser_doc_content(doc_path: str) -> str:

    if doc_path is None or not isinstance(doc_path, str) or doc_path.strip() == "":
        return "错误：文件路径不能为空"
    if not os.path.exists(doc_path):
        return f"错误：文件路径 '{doc_path}' 不存在"
    if os.path.isdir(doc_path):
        file_list = []
        try:
            for root, dirs, files in os.walk(doc_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    file_name = os.path.basename(file)  # 或者直接用 file 变量
                    file_list.append({
                        "name": file_name,
                        "path": full_path
                    })
            if not file_list:
                return f"提示：目录 '{doc_path}' 是空的，或者不包含任何文件。"
            total_count = len(file_list)
            displayed_files = file_list[:]

            result_msg = f"检测到目录 '{doc_path}'，共找到 {total_count} 个文件。\n"
            result_msg += "\n".join([
                f"- 文件名：{f['name']}\n  路径：{f['path']}"
                for f in displayed_files
            ])
            return result_msg
        except Exception as e:
            return f"错误：遍历目录时发生异常 - {str(e)}"

    elif os.path.isfile(doc_path):
        try:
            content = ""
            encodings = ['utf-8', 'gbk', 'latin-1']
            for enc in encodings:
                try:
                    with open(doc_path, 'r', encoding=enc) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            if not content and open(doc_path, 'rb').read():
                return f"提示：文件 '{doc_path}' 似乎是二进制文件或非文本文件，无法直接读取为文本内容。"

            file_name = os.path.basename(doc_path)
            return f"文件完整内容:\n{content}\n\n文件的名字：{file_name}\n文件的路径：{doc_path}"
        except Exception as e:
            return f"错误：读取文件 '{doc_path}' 时失败 - {str(e)}"

# doc_path:文件保存路径
# content：内容
# suffix：文件后缀
# file_name:文件名字
class FieldInfoWrite(BaseModel):
    doc_path:str = Field(description="文件保存的目录路径。如果目录不存在，工具会自动创建。例如：'./data' 或 '/home/user/docs'")
    content:str = Field(description="要写入文件的具体文本内容。")
    file_name:str = Field(description="文件的名称（不包含后缀）。例如：'report' 或 'config'")
    suffix:str = Field(default="",description="文件后缀，如 'py', 'txt'。若不传则尝试从文件名识别或默认为空。")
@tool(
    name_or_callable="write_doc_content",
    description=   "用于将文本内容写入到指定路径的文件中。\n"
        "主要功能：\n"
        "1. 如果目标文件不存在，会自动**新建**该文件。\n"
        "2. 如果目标文件已存在，会**覆盖**原有内容。\n"
        "3. 如果指定的目录不存在，会自动**创建目录**。\n"
        "适用场景：保存日志、生成报告、存储配置、导出数据等。\n"
        "注意：content 参数必须是字符串格式。",
    args_schema=FieldInfoWrite,
    return_direct=False
)
def write_doc_content(doc_path: str, content: str,file_name:str,suffix:str)->str:

    if not doc_path or not isinstance(doc_path, str):
        return "错误：保存路径不能为空"
    if not file_name or not isinstance(file_name, str):
        return "错误：文件名不能为空"

    content = str(content) if content is not None else ""

    clean_suffix = suffix.strip() if suffix else ""
    if clean_suffix and not clean_suffix.startswith('.'):
        clean_suffix = f".{clean_suffix}"

    full_path = os.path.join(doc_path, f"{file_name}{clean_suffix}")

    file_existed_before = os.path.exists(full_path)

    try:
        if not os.path.exists(doc_path):
            os.makedirs(doc_path, exist_ok=True)

        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)

        action_type = "新建" if not file_existed_before else "覆盖更新"

        return f"成功：文件已{action_type}。\n路径：{full_path}\n大小：{len(content)} 字符"

    except Exception as e:
        return f"错误：{str(e)}"