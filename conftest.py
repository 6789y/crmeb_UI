import pytest
from playwright.async_api import Page

from config import URL


@pytest.fixture
def get_page_func(page: Page):
    """获取page对象"""
    page.goto(URL)  # 开页面
    yield page  # 返回 page 对象
    page.close()  # 关闭页面
