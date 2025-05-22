from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

# 数据库连接配置
db_url = 'mysql+mysqlconnector://root:As984315#@42.194.236.54/darknet'
engine = create_engine(db_url)

# 查询数据，筛选出ntcp2_ipv4不为空的记录
query = """
SELECT firsttime, ntcp2_ipv6
FROM RouterInfo
WHERE NTCP2_ipv6 IS NOT NULL
  AND NTCP2_ipv6 != ''
  AND NTCP2_ipv6 REGEXP '^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$';

"""
df = pd.read_sql(query, engine)

# 将 firsttime 列转换为日期格式
df['firsttime'] = pd.to_datetime(df['firsttime'])

# 按天统计 ntcp2_ipv4 不为空的数据条数
daily_counts = df.groupby(df['firsttime'].dt.date).size()

# 计算截止到当天的总量
cumulative_counts = daily_counts.cumsum()

# 使用Seaborn样式来改进图形外观
plt.style.use('seaborn-darkgrid')  # 使用 seaborn 的 darkgrid 样式

# 创建图表
plt.figure(figsize=(12, 8))

# 绘制两条折线
plt.plot(daily_counts.index, daily_counts.values, marker='o', linestyle='-', color='b', linewidth=2, label='Daily Count')
plt.plot(cumulative_counts.index, cumulative_counts.values, marker='o', linestyle='-', color='g', linewidth=2, label='Cumulative Count')

# 添加标题和标签
plt.title('Daily and Cumulative Count of Non-Empty NTCP2 IPv6 Entries', fontsize=18, weight='bold')
plt.xlabel('Date', fontsize=14)
plt.ylabel('Count', fontsize=14)

# 设置X轴的日期格式
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)

# 添加网格线，增强图表的可读性
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# 添加图例
plt.legend()

# 设置背景色
plt.gcf().set_facecolor('#f9f9f9')

# 保存图表为图片文件
plt.savefig('ntcp2_ipv6_counts.png', dpi=300, bbox_inches='tight')  # 保存为高分辨率的PNG格式

# 显示图表
plt.tight_layout()
plt.show()
