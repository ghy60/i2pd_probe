from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 数据库连接配置
db_url = 'mysql+mysqlconnector://root:As984315#@42.194.236.54/darknet'
engine = create_engine(db_url)

# 查询数据
query = "SELECT updatetime FROM RouterInfo;"
df = pd.read_sql(query, engine)

# 将 updatetime 列转换为日期格式
df['updatetime'] = pd.to_datetime(df['updatetime'])

# 按天统计每一天的数据条数
daily_counts = df.groupby(df['updatetime'].dt.date).size()

# 使用Seaborn样式来改进图形外观
plt.style.use('seaborn-darkgrid')  # 使用 seaborn 的 darkgrid 样式

# 创建图表
plt.figure(figsize=(12, 8))

# 绘制折线图
daily_counts.plot(kind='line', marker='o', linestyle='-', color='b', linewidth=2)

# 添加标题和标签
plt.title('Daily Node Count Over Time', fontsize=18, weight='bold')
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

# 设置背景色
plt.gcf().set_facecolor('#f9f9f9')

# 保存图表为图片文件
plt.savefig('daily_counts_enhanced.png', dpi=300, bbox_inches='tight')  # 保存为高分辨率的PNG格式

# 显示图表
plt.tight_layout()
plt.show()
