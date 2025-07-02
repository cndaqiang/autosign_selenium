import sys
import time
import yaml  # 用于读取配置文件
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import check_timestamp

# ======================== 0. 初始化命令 ========================
check_timestamp.check(run_interval_hours=1e-6, run_interval_days=0)

# ======================== 1. 读取配置 ========================
# 配置文件 config.yml 示例：
# edge:
#   driver_path: D:/SoftData/edgedriver/msedgedriver.exe
#   user_data_dir: D:/SoftData/EdgeUserData

with open("config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Edge WebDriver 路径从配置文件读取
service = Service(executable_path=config["edge"]["driver_path"])

# ======================== 2. Edge 启动选项 ========================
edge_options = Options()

# 设置 Selenium 专用的用户数据目录（浏览器 Profile）
# 这里存储 Cookies / 登录态，下次可以自动复用
edge_options.add_argument(f"user-data-dir={config['edge']['user_data_dir']}")

# 启动时最大化窗口
edge_options.add_argument("--start-maximized")

# 固定窗口大小（无头模式或需要特定分辨率的页面很有用）
edge_options.add_argument("--window-size=1920,1080")

# 根据命令行参数决定是否用 GUI 模式：
# - 默认无头（headless），完全后台运行
# - 如果命令行包含 --gui，则以可视化界面运行
headless = True
if "--gui" in sys.argv:
    headless = False

if headless:
    edge_options.add_argument("--headless")

# ======================== 3. 创建 WebDriver ========================
driver = webdriver.Edge(service=service, options=edge_options)

try:
    # ======================== 4. 打开目标页面 ========================
    driver.get("https://www.ablesci.com/")

    # 如果是有头模式，需要手动扫码/登录
    if not headless:
        input("请在浏览器中完成登录后，按回车继续...")

    # ======================== 5. 全局隐式等待 ========================
    # 在调用 find_element / find_elements 时等待最多 10 秒
    driver.implicitly_wait(10)

    # ======================== 6. 查找签到按钮 ========================
    # 可能的按钮 HTML：
    # <button class="layui-btn layui-btn-danger btn-sign">今日打卡签到</button>
    # 或者 <a class="layui-btn layui-btn-danger btn-sign">今日打卡签到</a>

    # Selenium 选择器支持：
    # - 标签选择：button, a, input, div...
    # - 类选择：.btn-sign
    # - id 选择：#my-id
    # - 属性选择：a[href="javascript:;"]
    # - 组合：button.btn-sign 或 a.btn-sign
    #
    # find_elements 返回一个列表（即使没找到也不会报错，只是返回空列表）
    # find_element 如果没找到则抛出异常

    sign_buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn-sign")
    # sign_buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn-sign, a.btn-sign, input.btn-sign")
    # 说明：这里的 CSS 选择器支持同时匹配 <button>、<a>、<input> 中 class=btn-sign 的元素

    found = False
    for btn in sign_buttons:
        # 获取按钮文本内容并去掉首尾空白
        btn_text = btn.text.strip()
        print(f"检查按钮内容: {btn_text}")

        # 当页面含有多个 btn-sign 时，可使用：
        # - btn.get_attribute("id") 获取元素 id
        # - btn.get_attribute("class") 获取元素类名
        # - btn.text 获取元素可见文本
        #
        # 例如：
        # if btn.get_attribute("id") == "sign-btn-1":
        #     btn.click()

        # 这里用文本内容进行匹配，确保是正确的签到按钮
        if "今日打卡签到" in btn_text:
            print("确认是需要的签到按钮，正在点击...")
            btn.click()
            print("已点击签到按钮！")
            found = True
            break  # 找到后立即退出循环

    if not found:
        print("没有找到符合条件的签到按钮，可能今天已签到或页面状态异常。")

    # ======================== 7. 等待响应并截图 ========================
    # 等待几秒让签到结果返回，特别是有头模式下可观察
    time.sleep(5)

    # 截图保存当前页面
    driver.save_screenshot("sign_result.ablesci.png")
    print("截图已保存到 sign_result.png，请检查是否签到成功。")

finally:
    # ======================== 8. 退出浏览器 ========================
    print("签到结束. 退出浏览器")
    if not headless:
        input("按回车关闭浏览器...")
    driver.quit()
