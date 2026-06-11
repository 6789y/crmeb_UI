from playwright.async_api import Page

class GoodsShow:
    """商品详情页测试类"""
    def __init__(self, page:Page):
        self.page= page
    def goods_show(self):
        # 点击商品
        self.page.locator('#__layout > div > div:nth-child(2) > div.goodsSearch.wrapper_1200 > div.list.acea-row.row-middle > div > div.info.line2').click()
