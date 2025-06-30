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
    # 访问王者荣耀体验服活动页面
    # 这是腾讯王者荣耀体验服签到/兑换奖励的页面
    driver.get("https://pvp.qq.com/cp/a20161115tyf/page2.shtml")

    # 如果是有头模式，需要人工扫码登录 QQ，脚本会等待用户操作
    if not headless:
        input("👉 请在浏览器中完成登录后，按回车继续...")

    # 全局隐式等待（查找元素时最长等待10秒）
    driver.implicitly_wait(10)

    # 找到页面中所有可兑换的按钮：<a class="myexchange" value="...">兑换奖励</a>
    buttons = driver.find_elements(By.CSS_SELECTOR, "a.myexchange")

    for button in buttons:
        value = button.get_attribute('value')
        # 只点击 value=1 的兑换按钮
        if value == '1':
            print("✅ 找到 value=1 的按钮，正在点击...")
            button.click()
            break

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
