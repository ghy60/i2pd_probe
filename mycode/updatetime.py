from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
# 设置中文字体为 Noto Sans CJK TC
#plt.rcParams['font.family'] = 'Noto Sans CJK TC'

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

# 绘制可视化图表
plt.figure(figsize=(10, 6))
daily_counts.plot(kind='line', marker='o', linestyle='-', color='b')

# 设置图表标题和标签（中文）
plt.title('Count/Per day', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Node Count', fontsize=12)

# 美化日期显示
plt.xticks(rotation=45)
plt.grid(True)

# 保存图表为图片文件
plt.savefig('daily_counts.png')  # 保存为 PNG 格式

# 显示图表
plt.tight_layout()
plt.show()
