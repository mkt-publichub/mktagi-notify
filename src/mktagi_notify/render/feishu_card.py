"""飞书消息卡片 2.0。自定义机器人和应用机器人共用这一份对象。

外观约定见 wiki ``ai-env/notify.md``：标题栏按消息种类上色，正文两列字段，
底部一个跳转按钮指向主链接。
"""

from __future__ import annotations

from mktagi_notify.message import Message, Severity

_TEMPLATES = {
    Severity.INFO: "grey",
    Severity.SUCCESS: "green",
    Severity.WARNING: "orange",
    Severity.DANGER: "red",
}


def _fields(fields: dict[str, str]) -> dict:
    """两列字段：左列灰色字段名，右列字段值，逐行对应。"""
    names = "\n".join(f"<font color=grey>{key}</font>" for key in fields)
    values = "\n".join(fields.values())
    return {
        "tag": "column_set",
        "flex_mode": "bisect",
        "columns": [
            {
                "tag": "column",
                "width": "weighted",
                "weight": 1,
                "elements": [{"tag": "markdown", "text_size": "normal", "content": names}],
            },
            {
                "tag": "column",
                "width": "weighted",
                "weight": 1,
                "elements": [{"tag": "markdown", "text_size": "normal", "content": values}],
            },
        ],
    }


def card(message: Message) -> dict:
    """渲染成卡片对象。

    自定义机器人发的是 ``{"msg_type": "interactive", "card": <本对象>}``；
    应用机器人把本对象序列化成 ``content``。
    """
    elements: list[dict] = [{"tag": "markdown", "text_size": "normal", "content": message.text}]
    if message.fields:
        elements.append(_fields(message.fields))
    if message.url:
        elements.append(
            {
                "tag": "button",
                "type": "default",
                "size": "medium",
                "text": {"tag": "plain_text", "content": "查看详情"},
                "behaviors": [{"type": "open_url", "default_url": message.url}],
            }
        )

    return {
        "schema": "2.0",
        "config": {"update_multi": True},
        "header": {
            "title": {"tag": "plain_text", "content": message.title},
            "template": _TEMPLATES[message.severity],
        },
        "body": {
            "direction": "vertical",
            "padding": "12px 12px 12px 12px",
            "elements": elements,
        },
    }


def plain_text(message: Message) -> str:
    """卡片发不出去时的纯文本：标题、字段、正文，链接写在句末。"""
    lines = [message.title]
    lines.extend(f"{key}：{value}" for key, value in message.fields.items())
    lines.append(message.text)
    if message.url:
        lines.append(message.url)
    return "\n".join(lines)
