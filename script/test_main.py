from page.page01_login import Page1Login
from page.page02_search_goods import SearchGoods
from page.page03_goods_show import GoodsShow
from page.page04_goods_info import Page04GoodsInfo
from page.page05_goto_pay import Page05GotoPay


class TestMain:
    """测试类"""
    def test_main(self, get_page_func):
        """实例化测试方法"""
        self.page1_login = Page1Login(get_page_func)
        self.page2_search_goods = SearchGoods(get_page_func)
        self.page03_goods_show = GoodsShow(get_page_func)
        self.page04_goods_info = Page04GoodsInfo(get_page_func)
        self.page05_goto_pay = Page05GotoPay(get_page_func)
        """点击登录注册"""
        # 登录成功
        self.page1_login.login_method('19044972664', '12345678')
        # 输入商品
        self.page2_search_goods.input_goods('鲜花')
        # 点击搜索
        self.page2_search_goods.click_goods_search()
        #点击商品
        self.page03_goods_show.goods_show()
        # 选择商品规格A
        self.page04_goods_info.size_choose_a()
        # 商品数量加
        self.page04_goods_info.num_alter('2')
        #加入购物车
        self.page04_goods_info.cart_add()
        #进入购物车
        self.page04_goods_info.cart_enter()
        #去结算
        self.page05_goto_pay.goto_pay()



