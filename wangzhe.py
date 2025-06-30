import sys
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

# ---------------------------------------------------------------
# 该脚本基于Selenium和Edge浏览器自动化：
# 用于自动访问王者荣耀体验服的兑换页面 https://pvp.qq.com/cp/a20161115tyf/page2.shtml
# 自动点击value=1的“兑换奖励”按钮，实现每日签到/奖励领取。
#
# 脚本支持GUI模式（用于人工登录）和无头模式（自动后台运行）。
# 未来可以扩展到更多网站的签到、奖励领取等自动化脚本。
# ---------------------------------------------------------------

# 配置EdgeDriver，可通过微软官方下载并指定到本地路径
service = Service(executable_path=r"D:\GreenSoft\edgedriver_win64\msedgedriver.exe")

# 初始化Edge浏览器配置
edge_options = Options()

# 指定一个独立的用户数据目录，用于保存登录状态
# 这样下次运行脚本时，不必每次都重新扫码登录
edge_options.add_argument(r"user-data-dir=D:\GreenSoft\edgedriver_win64\selenium_edge_profile")

# 启动时最大化窗口（仅GUI模式下有意义）
edge_options.add_argument("--start-maximized")

# 设置浏览器窗口大小（即使在无头模式也能保证截图完整）
edge_options.add_argument("--window-size=1920,1080")

# 默认使用无头模式，以便在服务器或无人值守环境运行
headless = True

# 如果脚本启动时带了 --gui 参数，就使用有头模式方便人工调试
if "--gui" in sys.argv:
    headless = False

# 根据headless变量，决定是否添加无头参数
if headless:
    edge_options.add_argument("--headless")

# 创建Selenium Edge浏览器对象
driver = webdriver.Edge(service=service, options=edge_options)

try:
    # 打开王者荣耀体验服兑换奖励页面
    driver.get("https://pvp.qq.com/cp/a20161115tyf/page2.shtml")

    # 如果是GUI模式，需要等待用户扫码登录
    if not headless:
        input("👉 请在浏览器中完成QQ登录后，按回车继续...")

    # 设置隐式等待10秒，查找元素时最多等待10秒
    driver.implicitly_wait(10)

    # 查找所有兑换按钮：<a class="myexchange" value='...'>兑换奖励</a>
    buttons = driver.find_elements(By.CSS_SELECTOR, "a.myexchange")

    # 遍历按钮，找到 value=1 的按钮后点击
    for button in buttons:
        value = button.get_attribute('value')
        if value == '1':
            print("✅ 找到 value=1 的按钮，正在点击...")
            button.click()
            break  # 点击完即退出循环

    # 等待5秒，确保页面有时间响应
    time.sleep(5)

    # 保存当前页面截图到本地文件
    driver.save_screenshot("sign_result.png")
    print("✅ 截图已保存到 sign_result.png，请检查兑换结果。")

finally:
    # GUI模式下，为了方便手动查看结果，留住浏览器窗口
    if not headless:
        input("按回车关闭浏览器...")
    driver.quit()
