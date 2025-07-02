import json
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

driver = webdriver.Edge(service=service, options=edge_options)

try:
    print("Edge 浏览器已启动！")
    print("请在浏览器中自由访问并完成所有需要的登录。")
    print("完成后请回到命令行按回车，脚本将收集所有打开网页的cookies。")
    input("按回车开始收集 cookies...")

    all_cookies = {}

    # 遍历当前 session 里已知的所有窗口
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        current_url = driver.current_url
        if current_url.startswith("data:") or current_url == "about:blank":
            continue  # 排除空白或无效标签页
        domain = driver.execute_script("return document.domain")
        cookies = driver.get_cookies()
        if cookies:
            print(f"收集到域名 [{domain}] 的 {len(cookies)} 条 cookies")
            all_cookies[domain] = cookies

    with open("cookies.json", "w", encoding="utf-8") as f:
        json.dump(all_cookies, f, ensure_ascii=False, indent=2)
    print("所有 cookies 已保存到 cookies.json")
finally:
    driver.quit()
