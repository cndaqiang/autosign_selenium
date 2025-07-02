import json
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import yaml
import sys

# 读取配置文件
with open("config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

service = Service(executable_path=config["edge"]["driver_path"])

edge_options = Options()
edge_options.add_argument(f"user-data-dir={config['edge']['user_data_dir']}")
edge_options.add_argument("--start-maximized")

# 根据命令行参数决定是否用 GUI 模式：
# - 默认无头（headless），完全后台运行
# - 如果命令行包含 --gui，则以可视化界面运行
headless = True
if "--gui" in sys.argv:
    headless = False

if headless:
    edge_options.add_argument("--headless")

#
driver = webdriver.Edge(service=service, options=edge_options)



try:
    # 加载cookies文件
    with open("cookies.json", "r", encoding="utf-8") as f:
        all_cookies = json.load(f)

    for domain, cookies in all_cookies.items():
        url = f"https://{domain}/"
        print(f"访问 {url} 并注入 {len(cookies)} 个 cookies...")
        driver.get(url)
        time.sleep(3)  # 等待页面加载，防止注入失败

        # 删除原有cookies，避免冲突
        driver.delete_all_cookies()

        # 注入cookies
        for cookie in cookies:
            cookie_dict = {
                "name": cookie.get("name"),
                "value": cookie.get("value"),
                "domain": cookie.get("domain"),
                "path": cookie.get("path", "/"),
                "expiry": cookie.get("expiry"),
                "secure": cookie.get("secure", False),
                "httpOnly": cookie.get("httpOnly", False),
                "sameSite": cookie.get("sameSite") if "sameSite" in cookie else None,
            }
            # 删除值为 None 的键
            cookie_dict = {k: v for k, v in cookie_dict.items() if v is not None}
            try:
                driver.add_cookie(cookie_dict)
            except Exception as e:
                print(f"添加cookie {cookie_dict['name']} 失败：{e}")

        # 刷新页面让cookie生效
        driver.refresh()
        time.sleep(3)

    print("所有cookies已成功注入。你现在可以无须重新登录访问这些网站。")

finally:
    input("按回车退出并关闭浏览器...")
    driver.quit()
