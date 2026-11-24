from mktagi_notify import Message, Severity
from mktagi_notify.render.feishu_card import card, plain_text


def test_card_shape():
    payload = card(Message(title="Q/USDT 急拉", text="涨跌幅 **+5.39%**"))
    assert payload["schema"] == "2.0"
    assert payload["header"]["title"]["content"] == "Q/USDT 急拉"
    assert payload["header"]["template"] == "grey"
    assert payload["body"]["elements"] == [
        {"tag": "markdown", "text_size": "normal", "content": "涨跌幅 **+5.39%**"}
    ]


def test_severity_template():
    for severity, template in [
        (Severity.INFO, "grey"),
        (Severity.SUCCESS, "green"),
        (Severity.WARNING, "orange"),
        (Severity.DANGER, "red"),
    ]:
        payload = card(Message(title="t", text="x", severity=severity))
        assert payload["header"]["template"] == template


def test_fields_are_two_columns():
    payload = card(Message(title="t", text="x", fields={"时间": "13:37", "金额": "5 USDT"}))
    column_set = payload["body"]["elements"][1]
    assert column_set["tag"] == "column_set"
    left, right = column_set["columns"]
    assert (
        left["elements"][0]["content"]
        == "<font color=grey>时间</font>\n<font color=grey>金额</font>"
    )
    assert right["elements"][0]["content"] == "13:37\n5 USDT"


def test_url_is_bottom_button():
    payload = card(Message(title="t", text="x", fields={"a": "b"}, url="http://h/"))
    button = payload["body"]["elements"][-1]
    assert button["tag"] == "button"
    assert button["behaviors"] == [{"type": "open_url", "default_url": "http://h/"}]


def test_no_extra_elements_without_fields_or_url():
    payload = card(Message(title="t", text="x"))
    assert len(payload["body"]["elements"]) == 1


def test_plain_text_puts_url_last():
    text = plain_text(Message(title="标题", text="备注", fields={"金额": "5"}, url="http://h/"))
    assert text == "标题\n金额：5\n备注\nhttp://h/"
