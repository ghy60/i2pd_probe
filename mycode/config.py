import configparser
import os

# 创建一个配置解析器
config = configparser.RawConfigParser()  # 创建一个配置解析器，RawConfigParser()是configparser的子类，支持原始的配置文件格式

# 读取配置文件
config_path = "/root//i2pd_tance/mycode/config.ini"
config.read(config_path)