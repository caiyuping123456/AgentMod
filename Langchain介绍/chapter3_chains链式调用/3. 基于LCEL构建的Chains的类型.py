"""
    对应新型的chain都是驼峰形的，如以下：
    create_sql_query_chain
    create_stuff_documents_chain
    create_openai_fn_runnable
    create_structured_output_runnable
    load_query_constructor_runnable
    create_history_aware_retriever
    create_retrieval_chain
    这里值演示create_sql_query_chain和
"""
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.sql_database.query import create_sql_query_chain
## 演示create_sql_query_chain，这个是将自然语言（LLM）转为Sql查询语句的，具体的使用如下：
from langchain_community.utilities import SQLDatabase

# 连接 MySQL 数据库
db_user = "root"
db_password ="abc123"

# 根据自己的密码填写
db_host = "127.0.0.1"
db_port ="3306"
db_name ="atguigudb"
# mysql+pymysql://用户名:密码@ip地址:端口号/数据库名
# 读取数据库的数据
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port} / {db_name}")
# 这个是数据库的属性
print("哪种数据库：", db.dialect)
print("获取数据表：", db.get_usable_table_names())
# 执行查询
res = db.run("SELECT count(*) FROM employees;")
print ("查询结果：", res)

## 调用大模型
import os

import dotenv
from langchain_core.messages import SystemMessage
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatMessagePromptTemplate, ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI

# 使用配置文件方式
dotenv.load_dotenv() # 一定要加这个（使用配置文件）===> 加载配置文件
chat = ChatOpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
    model=os.getenv("MODEL_NAME")
)

# 调用Chain
chain = create_sql_query_chain(llm=chat, db=db)
# response = chain.invoke({"question": "数据表employees中哪个员工工资高？"})
# print(response)
# response = chain.invoke({"question": "查询departments表中一共有多少个部门？"})
# print(response)
# response = chain.invoke({"question": "查询last_name叫King的基本情况"})
# print(response)
# # 限制使用的表
response = chain.invoke({"question": "一共有多少个员工？", "table_names_to_use": ["employees"]})
print(response)


# create_stuff_documents_chain的使用
"""
    create_stuff_documents_chain用于将
            多个文档内容合并成
            LLM处理（而不是分多次处理）。
            适合场景：
            单个长文本的链式工具，并一次性传递给 
            保持上下文完整，适合需要全局理解所有文档内容的任务（如总结、问答）
            适合处理 少量/中等长度文档 的场景
"""
# 举例

from langchain_core.documents import Document

# 定义提示词模板
prompt = PromptTemplate.from_template(
        """
        如下文档{docs}中说，香蕉是什么颜色的？
        """
)
# 创建链
# document_variable_name这个是文档的名字（要和提示词模板对应）
# injiijjnigyft和包含
chain = create_stuff_documents_chain(chat, prompt, document_variable_name="docs")
# 文档输入
docs = [Document(page_content=
        "苹果，学名Malus pumila Mill.，别称西洋苹果、柰，属于蔷薇科苹果属的植物。苹果是全球最广泛种植和销售的水果之一，具有悠久的栽培历史和广泛的分布范围。苹果的原始种群主要起源于中亚的天山山脉附近，尤其是现代哈萨克斯坦的阿拉木图地区，提供了所有现代苹果品种的基因库。苹果通过早期的贸易路线，如丝绸之路，从中亚向外扩散到全球各地。"),
        Document(page_content="香蕉是白色的水果，主要产自热带地区。"),
        Document(page_content="蓝莓是蓝色的浆果，含 有抗氧化物质。")
]
# 执行摘要
re = chain.invoke({"docs": docs})
print(re)
