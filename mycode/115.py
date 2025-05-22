from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 数据库连接配置
db_url = 'mysql+mysqlconnector://root:As984315#@42.194.236.54/darknet'
engine = create_engine(db_url)

# 查询数据，限制日期到 2025-01-15
query = """
SELECT firsttime 
FROM RouterInfo 
WHERE firsttime <= '2025-03-03';
"""
df = pd.read_sql(query, engine)

# 将 firsttime 列转换为日期格式
df['firsttime'] = pd.to_datetime(df['firsttime'])

# 按天统计每一天的数据条数
daily_counts = df.groupby(df['firsttime'].dt.date).size()

# 计算从1月3日到每一天的累计数据条数
# 获取最早的日期作为起始点
start_date = df['firsttime'].min().date()

# 创建一个新的 DataFrame 用于存储累计数据
cumulative_counts = daily_counts.cumsum()

# 使用Seaborn样式来改进图形外观
plt.style.use('seaborn-darkgrid')  # 使用 seaborn 的 darkgrid 样式

# 创建图表
plt.figure(figsize=(12, 8))

# 绘制第一条折线图：每日数据条数
daily_counts.plot(kind='line', marker='o', linestyle='-', color='b', linewidth=2, label='Daily Node Count')

# 绘制第二条折线图：累计数据条数
cumulative_counts.plot(kind='line', marker='x', linestyle='-', color='r', linewidth=2, label='Cumulative Node Count')

# 添加标题和标签
plt.title('Daily and Cumulative Node Count Over Time', fontsize=18, weight='bold')
plt.xlabel('Date', fontsize=14)
plt.ylabel('Node Count', fontsize=14)

# 设置X轴的日期格式
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)

# 添加网格线，增强图表的可读性
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# 添加数据点的标签
for x, y in zip(daily_counts.index, daily_counts):
    plt.text(x, y, f'{y}', color='black', ha='center', va='bottom', fontsize=10)

# 添加累计数据点的标签
for x, y in zip(cumulative_counts.index, cumulative_counts):
    plt.text(x, y, f'{y}', color='red', ha='center', va='bottom', fontsize=10)

# 设置背景色
plt.gcf().set_facecolor('#f9f9f9')

# 添加图例
plt.legend()

# 保存图表为图片文件
plt.savefig('first_enhanced_with_cumulative.png', dpi=300, bbox_inches='tight')  # 保存为高分辨率的PNG格式

# 显示图表
plt.tight_layout()
plt.show()
