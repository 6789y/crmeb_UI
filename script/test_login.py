import allure
import pytest
from common.read_login_json import get_test_login_data
from page.page01_login import Page1Login


class TestLogin:

    @pytest.mark.parametrize('username,password,expect,type', get_test_login_data())
    def test_login(self, get_page_func, username, password, expect, get_alert, type):
      with allure.step('登录测试'):
        self.page01_login = Page1Login(get_page_func)
        self.page01_login.login_method(username, password)
        if type=='pass':

            get_page_func.wait_for_timeout(10000)
            title = get_page_func.title()# 获取当前页面的标题(内置方法)
            assert expect in title
        elif type=='fail':
            # 获取弹窗的文本,以msg接收
            msg=get_alert.text()
            # print('\n',msg)
            assert expect in msg




