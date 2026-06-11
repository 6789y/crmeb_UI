from playwright.sync_api import Page


SEARCH_GOODS=('textbox', '搜索商品')
class SearchGoods:
    """搜索商品"""

    def __init__(self,page:Page):
        self.page= page
    def input_goods(self,goods):
        """输入商品"""
        self.page.get_by_role(role=SEARCH_GOODS[0], name=SEARCH_GOODS[1]).fill(goods)
    def click_goods_search(self):
        """点击商品"""
        self.page.locator('#__layout > div > div:nth-child(1) > div.nav.min_wrapper_1200 > div > div.search.acea-row.row-between-wrapper > div.bnt.bg-color').click()

