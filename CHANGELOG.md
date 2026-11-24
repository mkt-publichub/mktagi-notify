# 变更记录

格式沿用 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号是 `X.Y.Z` 语义化版本：不兼容的改动升 X，新能力升 Y，修 bug 升 Z。

## [0.0.2] - 2026-11-24

### 变更

- 飞书卡片外观：标题栏按 `severity` 上色（`INFO` 由蓝改灰），字段改两列（灰色字段名 + 值），`url` 改为底部「查看详情」跳转按钮。
- `FeishuWebhook` 卡片发不出去（请求失败或回执 `code` 非 0）时回退发纯文本，链接写在句末；纯文本也失败才抛错。
- 仓库迁到 `mkt-publichub/mktagi-notify`，项目链接同步。

### 新增

- `mktagi_notify.render.feishu_card.plain_text`。

## [0.0.1] - 2026-10-18

### 新增

- `Message`、`Severity`、`DeliveryResult` 三个类型，`Channel` 协议，`fanout` 并发分发。
- 五个通道：`FeishuWebhook`（自定义机器人，自算签名）、`FeishuBot`（应用机器人，官方 `lark-oapi`）、`Telegram`（`python-telegram-bot`）、`Slack`（官方 `slack-sdk`）、`Discord`（`discord.py`）。
- `from_env()` 按环境变量装配通道，凭据不全的通道自动跳过。
- 四个纯函数渲染器：飞书卡片 2.0、Telegram HTML、Discord embed、Slack Block Kit。
