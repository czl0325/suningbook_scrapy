# -*- coding: utf-8 -*-
import scrapy
from scrapy_test.items import SunningBookItem
import re

class SuningspiderSpider(scrapy.Spider):
    name = 'suningspider'
    allowed_domains = ['suning.com']
    # start_urls = ['https://book.suning.com/?safp=d488778a.10038.searchPathbox.1']
    start_urls = ['https://list.suning.com/1-502320-0.html']

    def parse(self, response):
        # menus = response.xpath("//div[@class='menu-item']//dd//a")
        # for menu in menus:
        #     item = SunningBookItem()
        #     item["category"] = menu.xpath("./text()").extract_first()
        #     href = menu.xpath("./@href").extract_first()
        #     yield scrapy.Request(
        #         href,
        #         callback=self.parse_booklist,
        #         meta={"item" : item}
        #     )
        item = SunningBookItem()
        li_list = response.xpath("//ul[@class='clearfix']/li")
        for li in li_list:
            item["cover"] = li.xpath("//div[@class='wrap']//div[@class='res-img']//a//img[@class='search-loading']/@src2").extract_first()
            item["title"] = li.xpath(".//div[@class='wrap']//p[@class='sell-point']/a/text()").extract_first()
            p_id1 = li.xpath(".//div[@class='wrap']/input/@vendor").extract_first()
            p_id2 = li.xpath(".//div[@class='wrap']/input/@datapro").extract_first()
            p_id2 = re.sub("[^\d]*\d*$", "", p_id2)
            p_id2 = re.sub("^[^\d]*", "", p_id2)
            detail_url = "https://product.suning.com/{}/{}.html".format(p_id1, p_id2)
            yield scrapy.Request(
                detail_url,
                callback=self.book_detail,
                meta={"item": item}
            )

    def parse_booklist(self, response):
        item = response.meta.get("item")
        li_list = response.xpath("//ul[@class='clearfix']/li")
        for li in li_list:
            print(li.xpath("//div[@class='wrap']//div[@class='res-img']//a//img[@class='search-loading']/@src2").extract_first())
            item["cover"] = li.xpath("//div[@class='wrap']//div[@class='res-img']//a//img[@class='search-loading']/@src").extract_first()
            item["cover"] = "https://" + item["cover"] if item["cover"] != None else ""
            item["title"] = li.xpath(".//div[@class='wrap']//p[@class='sell-point']/a/text()").extract_first()
            item["price"] = li.xpath(".//div[@class='wrap']//p[@class='prive-tag']/em//text()").extract()
            print(item)

    def book_detail(self, response):
        print(response.url)
        item = response.meta.get("item")
        # //*[@id="mainPrice"]/dl[1]/dd/span[1]
        price = response.xpath("//*[@id='mainPrice']/dl[1]/dd/span[1]//text()")
        print("价格=", price)
