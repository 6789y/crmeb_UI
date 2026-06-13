from playwright.async_api import Page

from common.log_config import log_config

# 此处存放所有元素的定位特征值信息
# 习惯使用常量保存信息:变量名全大写变量
LOGIN_BTN=('link','登录/注册')
USERNAME_LOGIN_CLICK='#__layout > div > div > div.loginBg.min_wrapper_1200 > div:nth-child(1) > div.fastLogin.font-color'
PHONE_INPUT=('textbox', '请输入手机号')
PASSWORD_INPUT=('textbox', '请输入密码')

class Page1Login:
    """
    登录页面
    """
    # 类属性后的方法访问类属性,省去了page参数
    def __init__(self, page: Page):
        self.page = page
        # 类属性日志
        self.log=log_config()
    # ================= 封装元素定位信息 =================
    #封装元素定位方法
    def find_by_role(self, role, name):
        return self.page.get_by_role(role=role, name=name)
    def find_locator(self, locator):
        return self.page.locator(locator)

    def login_btn(self):
        # 点击登录注册
        #调用封装的定位方法
        self.find_by_role(role=LOGIN_BTN[0], name=LOGIN_BTN[1]).click()
    def username_login_click(self):
        # 点击用户登录
        #调用封装的定位方法
        self.find_locator(USERNAME_LOGIN_CLICK).click()
    def phone_input(self, phone=None):
        # 输入手机号
        #调用封装的定位方法
        self.log.info(f'输入手机号{ phone}')
        self.find_by_role(role=PHONE_INPUT[0], name=PHONE_INPUT[1]).fill(phone)
    def password_input(self, password=None):
        # 输入密码
        #未调用封装的定位方法
        self.log.info(f'输入密码{ password}')
        self.page.get_by_role(role='textbox', name='请输入密码').fill(password)
    def contract_login_click(self):
        # 同意政策
        self.page.locator('#__layout > div > div > div.loginBg.min_wrapper_1200 > div:nth-child(2) > div.isAgree > label > span > span').click()
    def login_click(self):
        # 点击登录
        self.page.locator('#__layout > div > div > div.loginBg.min_wrapper_1200 > div:nth-child(2) > div.signIn.bg-color').click()

    # ================= 集合调用 =================
    def login_method(self, username, password):
        """登录成功"""
        self.login_btn()
        self.username_login_click()
        self.phone_input(username)
        self.password_input(password)
        self.contract_login_click()
        self.login_click()
