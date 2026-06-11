from page.page01_login import Page1Login
from page.page02_search_goods import SearchGoods
from page.page03_goods_show import GoodsShow

class TestLogin:
    """登录测试类"""
    def test_login(self, get_page_func):
        """实例化测试方法"""
        self.page1_login = Page1Login(get_page_func)
        self.page2_search_goods = SearchGoods(get_page_func)
        self.page03_goods_show = GoodsShow(get_page_func)
        """点击登录注册"""
        self.page1_login.login_btn()
        # 切换手机号登录
        self.page1_login.username_login_click()
        # 输入手机号
        self.page1_login.phone_input('19044972664')
        # 输入密码
        self.page1_login.password_input('12345678')
        #同意协议
        self.page1_login.contract_login_click()
        # 点击登录
        self.page1_login.login_click()
        # 输入商品
        self.page2_search_goods.input_goods('鲜花')
        # 点击搜索
        self.page2_search_goods.click_goods_search()
        #点击商品
        self.page03_goods_show.goods_show()
