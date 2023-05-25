import scrapy


class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["www.amazon.in"]
    start_urls = ["https://www.amazon.in/s?k=bags&ref=sr_pg_8"]

    def parse(self, response):
        products = response.css('div.s-main-slot.s-result-list.s-search-results.sg-row > div')
        for i in range(len(products)):
            link = products[i].css('a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal::attr(href)').get()
            name = products[i].css('.s-line-clamp-2 .a-text-normal').get()
            prize = products[i].css('.puis-padding-right-base .a-price-whole').get()
            no_of_ratings = products[i].css('.s-link-style .s-underline-text').get()

            if link is None: continue
            response.follow(link, callback = self.page_parse)

            yield({
                'link' : link,
                'name' : name,
                'prize' : prize,
                'no_of_ratings' : no_of_ratings
            })
    
    def page_parse(self, response):
        image = response.css('div[id=imgTagWrapperId] > img::attr(src)').get()
        ASIN = response.css(
            'div[id=detailBullets_feature_div] > ul.a-unordered-list.a-nostyle.a-vertical.a-spacing-none.detail-bullet-list.li:nth-child(4).a-text-bold+span::text').get()
        manufacturer = response.css(
            'div[id=detailBullets_feature_div] > ul.a-unordered-list.a-nostyle.a-vertical.a-spacing-none.detail-bullet-list.li:nth-child(3).a-text-bold+ span::text').get()
        product_dimension = response.css(
            'div[id=detailBullets_feature_div] > ul.a-unordered-list.a-nostyle.a-vertical.a-spacing-none.detail-bullet-list.li:nth-child(1) .a-text-bold+ span::text').get()
        
        yield({
            'image': image,
            'asin' : ASIN,
            'manufacturer': manufacturer,
            'product_dimension': product_dimension,
        })

