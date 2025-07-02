import sys
import time
import yaml  # 用于读取配置文件
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

# 读取配置文件（config.yml）
# 通过 config_example.yml 提供示例，用户需要复制为 config.yml 并修改
with open("config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Edge WebDriver 路径，从 config.yml 读取
service = Service(executable_path=config["edge"]["driver_path"])

# 配置 Edge 启动选项
edge_options = Options()

# 指定 Selenium 专用的用户数据目录（浏览器 Profile）：
# - 这里存储 QQ 登录信息、Cookies
# - 下次运行可以复用登录状态
edge_options.add_argument(f"user-data-dir={config['edge']['user_data_dir']}")

# 启动时最大化窗口
edge_options.add_argument("--start-maximized")

# 设置固定窗口大小（无头模式下尤其需要）
edge_options.add_argument("--window-size=1920,1080")

# 创建 Edge 浏览器实例
driver = webdriver.Edge(service=service, options=edge_options)

try:
    # 打开浏览器
    driver.get("https://www.bing.com")

    input("👉 请在浏览器中完成相关网站登录后，按回车退出")
finally:
    driver.quit()
