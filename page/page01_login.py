from playwright.async_api import Page

from conftest import get_page_func

LOGIN_BTN=('link','登录/注册')
USERNAME_LOGIN_CLICK='#__layout > div > div > div.loginBg.min_wrapper_1200 > div:nth-child(1) > div.fastLogin.font-color'
PHONE_INPUT=('textbox', '请输入手机号')
PASSWORD_INPUT=('textbox', '请输入密码')

class Page1Login:
    """
    登录页面
    """
    def __init__(self, page: Page):
        self.page = page

    def login_btn(self):
        # 点击登录注册
        self.page.get_by_role(role=LOGIN_BTN[0], name=LOGIN_BTN[1]).click()
    def username_login_click(self):
        # 输入用户名
        self.page.locator(USERNAME_LOGIN_CLICK).click()
    def phone_input(self, phone):
        # 输入手机号
        self.page.get_by_role(role=PHONE_INPUT[0], name=PHONE_INPUT[1]).fill(phone)
    def password_input(self, password):
        # 输入密码
        self.page.get_by_role(role='textbox', name='请输入密码').fill(password)
    def contract_login_click(self):
        # 同意政策
        self.page.locator('#__layout > div > div > div.loginBg.min_wrapper_1200 > div:nth-child(2) > div.isAgree > label > span > span').click()
    def login_click(self):
        # 点击登录
        self.page.locator('#__layout > div > div > div.loginBg.min_wrapper_1200 > div:nth-child(2) > div.signIn.bg-color').click()


if __name__ == '__main__':
    a=Page1Login(get_page_func)
    a.login_btn()