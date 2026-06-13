
from pydoc import text

import pytest
from playwright.async_api import Page

from config import URL


@pytest.fixture
def get_page_func(page: Page):
    """获取page对象"""
    page.goto(URL)  # 开页面
    yield page  # 返回 page 对象
    page.close()  # 关闭页面

@pytest.fixture
def get_alert(page: Page):
    """获取弹窗操作对象"""

    class AlertHelper:
        # 弹窗操作类, 封装弹窗操作
        def __init__(self, page):
            self.page = page

        def text(self):
            """获取弹窗文本内容"""
            return self.page.locator('body > div.el-message.el-message--error.el-message-fade-leave-active.el-message-fade-leave-to > p').text_content()
    return AlertHelper(page)