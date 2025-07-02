# autosign_selenium

一个基于 Selenium 的自动化签到脚本，用于在网页上进行每日签到/兑换奖励。

## 功能简介

- 在 Edge 浏览器中模拟登录、访问签到页面。
- 根据按钮自动点击指定奖励。
- 自动保存签到结果截图。
- 通过配置文件管理 WebDriver 路径和浏览器数据目录。
- 支持：
  - 有头模式（带GUI，可手动登录调试）
  - 无头模式（自动化运行，完全后台执行）

## 使用方法
0. 安装 [Microsoft Edge WebDriver](https://developer.microsoft.com/microsoft-edge/tools/webdriver/)，版本要和你本地 Edge 浏览器版本一致。



1. 安装 Python 和依赖：
```bash
   pip install selenium pyyaml
````

2. 准备 Edge WebDriver 并下载与系统 Edge 浏览器版本一致的 `msedgedriver.exe`。

3. 创建配置文件：

   * 将 `config_example.yml` 复制为 `config.yml`
   * 根据你本机环境修改其中的 `driver_path` 和 `user_data_dir`

4. 运行脚本：

   * 自动化无头运行：

     ```
     python www.ablesci.com.py
     ```
    
   * 带GUI调试（需要手动登录以保存cookies）：

     ```
     python www.ablesci.com.py --gui
     ```

5. 查看 `sign_result.png` 截图文件以确认签到结果。

## 项目结构

```
├── edge.py                 打开edge浏览器进行登录调试
├── www.ablesci.com.py      www.ablesci.com签到
├── config_example.yml      示例配置文件
├── .gitignore              忽略 config.yml 和中间产物
└── README.md               项目说明文件
```


---

**作者声明：** 本项目脚本和README由 OpenAI 的 ChatGPT 辅助编写，并经过个人调试优化。