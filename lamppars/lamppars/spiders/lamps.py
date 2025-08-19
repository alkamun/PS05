import scrapy


class LampsSpider(scrapy.Spider):
    name = "lamps"
    allowed_domains = ["https://divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]

    def parse(self, response):
        lamps = response.css('div.WdR1o')

        for lamp in lamps:
            yield {
                'name' : lamp.css('div.lsooF span::text').get(),
                'price' : lamp.css('div.pY3d2 span::text').get(),
                'url' : lamp.css('a').attrib['href']
            }
