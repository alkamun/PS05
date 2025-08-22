import scrapy

class LampsSpider(scrapy.Spider):
    name = "lamps"
    allowed_domains = ["divan.ru"]
    url = "https://www.divan.ru"
    start_urls = [url + "/category/svet"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            cb_kwargs={"page": None}
        )

    def parse(self, response, page):
        lamps = response.css('div.WdR1o')

        for lamp in lamps:
            price = ''.join([c for c in lamp.css('div.pY3d2 span::text').get() if c.isalnum()])
            a = lamp.css('a')
            href = a.attrib['href'] if a else None
            yield {
                'name' : lamp.css('div.lsooF span::text').get().strip(),
                'price' : price,
                'url' : self.url + href if href else ""
            }

        if not page:
            page = 2
        else:
            page = page + 1

        next_url = f"{self.start_urls[0]}/page-{page}"

        links = response.css('a.PaginationLink')
        page_link = None

        for link in links:
            page_link = self.url + link.attrib['href']
            if page_link == next_url:
                break

        if page_link:
            yield response.follow(page_link, self.parse, cb_kwargs={"page": page})
