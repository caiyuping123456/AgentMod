# 导入所需库
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 读取IMDB电影数据文件
movie = pd.read_csv("IMDB-Movie-Data.csv")

# 计算唯一导演的数量并打印
director_num = np.unique(movie['Director']).shape[0]
print(f"唯一导演的数量：{director_num}")

# 绘制电影评分分布的直方图
# 创建画布，设置尺寸和分辨率
plt.figure(figsize=(20, 8), dpi=100)
# 绘制直方图，将评分数据分成20个区间
plt.hist(movie["Rating"].values, bins=20)

# 设置x轴刻度：从评分最小值到最大值生成21个刻度点
max_ = movie["Rating"].max()
min_ = movie["Rating"].min()
tl = np.linspace(min_, max_, num=21)
plt.xticks(tl)

# 添加网格线提升可读性
plt.grid()
# 显示绘制的图表
plt.show()

# 提取电影时长数据
runtime_data = movie["Runtime (Minutes)"]

# 创建画布，设置尺寸和分辨率
plt.figure(figsize=(20, 8), dpi=80)

# 计算时长的最大值、最小值，确定直方图的区间数
max_ = runtime_data.max()
min_ = runtime_data.min()
num_bin = (max_ - min_) // 5  # 用整数除法避免区间数为浮点数

# 绘制电影时长的直方图
plt.hist(runtime_data, num_bin)

# 设置x轴刻度，步长为5
plt.xticks(range(min_, max_ + 5, 5))

# 添加网格线，提升图表可读性
plt.grid()

# 显示图表
plt.show()

# ========== 核心：自定义分箱逻辑 ==========
# 方法1：按固定步长5分钟手动生成分箱区间（推荐，和你原逻辑一致）
min_runtime = runtime_data.min()
max_runtime = runtime_data.max()
# 生成从最小值到最大值、步长为5的分箱区间（左闭右开）
bins = np.arange(min_runtime, max_runtime + 5, 20)

# 方法2：也可以手动指定自定义区间（比如按观影时长分段）
# bins = [60, 80, 100, 120, 140, 160, 180]  # 示例：短/中/长/超长电影

# ========== 绘制分箱后的直方图 ==========
plt.figure(figsize=(10, 8), dpi=80)
# 传入自定义bins，edgecolor显示区间边框，更清晰
plt.hist(runtime_data, bins=bins, edgecolor='black', alpha=0.7)

# 设置x轴刻度与分箱区间对齐
plt.xticks(bins)

# 添加标签和标题（提升可读性）
plt.xlabel("电影时长（分钟）", fontsize=12)
plt.ylabel("电影数量", fontsize=12)
plt.title("IMDB电影时长分布直方图（5分钟/区间）", fontsize=30)

plt.grid(axis='y', alpha=0.3)  # 仅显示y轴网格，避免x轴刻度重叠
plt.show()

# 1. 查看电影评分的平均值
rating_mean = movie["Rating"].mean()
print("电影评分的平均值：", rating_mean)

# 2. 查看唯一导演的人数（两种方法）
# 方法1：使用numpy的unique函数
director_count_np = np.unique(movie["Director"]).shape[0]
# 方法2：将导演列转为列表后去重，再计算长度
director_count_py = len(set(movie["Director"].tolist()))
print("唯一导演人数（numpy方法）：", director_count_np)
print("唯一导演人数（Python集合方法）：", director_count_py)

# 3. 查看唯一演员的人数
# 将演员列按逗号分割，转为嵌套列表
num = movie["Actors"].str.split(',').tolist()
# 展开嵌套列表，得到所有演员的一维列表（注意去除空格，避免因空格导致重复）
actor_nums = [j.strip() for i in num for j in i]
# 去重后计算唯一演员数量
actor_count = len(set(actor_nums))
print("唯一演员人数：", actor_count)

print(movie["Genre"].head())
