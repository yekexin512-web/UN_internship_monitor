# UN Internship Monitor

一个用于监控 UN Careers 实习岗位的 Python 工具。脚本会抓取 Category 为 Internship 的最新岗位，保存到 SQLite，并通过微信推送每日摘要。

## 功能

- 抓取 UN Careers 上 Category 为 Internship 的岗位。
- 提取岗位名、Job ID、部门、地点、发布日期、截止日期和申请链接。
- 保存岗位数据到 SQLite。
- 生成两类提醒：
  - A. 今日发布岗位
  - B. 明天截止岗位
- 支持通过 ServerChan 或企业微信机器人推送到微信。
- 支持 Windows 计划任务每日自动运行。

## 安装

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
Copy-Item .env.example .env
```

## 配置

编辑 `.env`：

```dotenv
PUSH_CHANNEL=serverchan
SERVERCHAN_SENDKEY=你的ServerChanSendKey
```

如果使用企业微信机器人：

```dotenv
PUSH_CHANNEL=wecom
WECOM_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=...
```

不要把 `.env` 上传到 GitHub。它包含你的微信推送密钥。

## 运行

只抓取并打印摘要，不推送：

```powershell
python -m un_intern_monitor.main --no-push
```

抓取并推送到微信：

```powershell
python -m un_intern_monitor.main
```

## 自动推送

Windows 可以使用计划任务每天运行：

```powershell
$project = "D:\儿童医保\Pythonproject"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$project\scripts\run_monitor.ps1`""
$trigger = New-ScheduledTaskTrigger -Daily -At 16:00
Register-ScheduledTask -TaskName "UNInternshipMonitor" -Action $action -Trigger $trigger -Description "Daily UN Careers internship monitor"
```

## 数据

岗位数据保存在：

```text
data/un_internships.sqlite
```

数据库文件是本地运行数据，不建议上传到 GitHub。
