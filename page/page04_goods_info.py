from playwright.async_api import Page


class Page04GoodsInfo:
    """商品详情页测试类"""
    def __init__(self, page:Page):
        self.page= page
    def get_coupon(self):
        """获取优惠券"""
        self.page.get_by_role(role='button', name='领取').click()
    def size_choose_a(self):
        """选择商品规格A"""
        self.page.locator('#__layout > div > div.goods-detail > div.wrapper_1200.acea-row > div.goods-main > div.acea-row.row-top > div.text-wrapper > div.attribute > div > div.acea-row.list > label:nth-child(1) > div > div.acea-row.row-middle.name').click()
    def num_add(self):
        """商品数量加"""
        self.page.locator('#__layout > div > div.goods-detail > div.wrapper_1200.acea-row > div.goods-main > div.acea-row.row-top > div.text-wrapper > div.number-wrapper.acea-row > div.counter-wrap > div > button.iconfont.icon-shangpinshuliang-jia').click()
    def num_alter(self, num):
        """点击商品数量修改"""
        self.page.locator('#__layout > div > div.goods-detail > div.wrapper_1200.acea-row > div.goods-main > div.acea-row.row-top > div.text-wrapper > div.number-wrapper.acea-row > div.counter-wrap > div > input').click()
        self.page.locator('#__layout > div > div.goods-detail > div.wrapper_1200.acea-row > div.goods-main > div.acea-row.row-top > div.text-wrapper > div.number-wrapper.acea-row > div.counter-wrap > div > input').fill(num)
    def cart_add(self):
        """加入购物车"""
        self.page.get_by_role(role='button', name='加入购物车').click()
    def cart_enter(self):
        """进入购物车"""
        self.page.locator('#__layout > div > div:nth-child(1) > div.header.min_wrapper_1200 > div > div > a.cartNum.on').click()
