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

# 根据命令行参数决定是否用 GUI 模式
# - 默认无头(headless)，完全后台运行
# - 如果命令中包含 --gui，则以有界面方式运行
headless = True
if "--gui" in sys.argv:
    headless = False

# 如果是无头模式，增加 headless 参数
if headless:
    edge_options.add_argument("--headless")

# 创建 Edge 浏览器实例
driver = webdriver.Edge(service=service, options=edge_options)

try:
    # 访问 Ablesci 网站
    driver.get("https://www.ablesci.com/")

    # 如果是有头模式，需要手动完成登录
    if not headless:
        input("👉 请在浏览器中完成登录后，按回车继续...")

    # 全局隐式等待（查找元素时最长等待10秒）
    driver.implicitly_wait(10)

    # 查找 Ablesci 今日签到按钮
    # <button class="layui-btn layui-btn-danger btn-sign">今日打卡签到</button>
    sign_button = driver.find_element(By.CSS_SELECTOR, "button.btn-sign")

    if sign_button:
        print("✅ 找到今日打卡签到按钮，正在点击...")
        sign_button.click()
        print("🎉 已点击签到按钮！")
    else:
        print("❌ 没有找到签到按钮，请检查页面状态或是否已签到。")

    # 等待几秒，方便观察结果（特别是有头模式）

    # 等待页面响应结果
    time.sleep(5)

    # 截图保存当前页面，用于后续人工核对
    driver.save_screenshot("sign_result.png")
    print("✅ 截图已保存到 sign_result.png，请检查是否兑换成功。")

finally:
    # 如果是有头模式，给用户留时间查看结果
    if not headless:
        input("按回车关闭浏览器...")
    driver.quit()
