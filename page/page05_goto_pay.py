from playwright.async_api import Page


class Page05GotoPay:
    """商品详情页测试类"""
    def __init__(self, page:Page):
        self.page= page
    def goto_pay(self):
        """点击去结算"""
        self.page.locator('#__layout > div > div.shoppingCart.wrapper_1200 > div.footer.acea-row.row-between-wrapper > div.acea-row.row-middle > div.bnt.bg-color').click()
