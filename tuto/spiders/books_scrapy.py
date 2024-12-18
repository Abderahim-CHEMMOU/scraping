# import scrapy

# class BookspiderSpider(scrapy.Spider):
#     name = 'books'
#     start_urls = ['https://books.toscrape.com/']

#     def parse(self, response):
#         books = response.css('article.product_pod')
#         for book in books:
#             yield{
#                 'name' : book.css('h3 a ::attr(title)').get(),
#                 'price' : book.css('div.product_price .price_color::text').get(),
#                 'url' : book.css('h3 a').attrib['href'],
#             }
        
#         next_page = response.css('li.next a ::attr(href)').get()
#         if next_page is not None:
#             if 'catalogue/' in next_page:
#                 next_page_url = 'https://books.toscrape.com/' + next_page
#             else:
#                 next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
#             yield response.follow(next_page_url, callback=self.parse)


import scrapy

class BookspiderSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            relative_url = book.css('h3 a').attrib['href']
            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            yield scrapy.Request(book_url, callback=self.parse_book_page)

        ## Next Page        
        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self, response):
        book = response.css("div.product_main")[0]
        table_rows = response.css("table tr")
        yield {
            # 'url': response.url,
            'title': book.css("h1 ::text").get(),
            # 'upc': table_rows[0].css("td ::text").get(),
            # 'product_type': table_rows[1].css("td ::text").get(),
            # 'price_excl_tax': table_rows[2].css("td ::text").get(),
            # 'price_incl_tax': table_rows[3].css("td ::text").get(),
            # 'tax': table_rows[4].css("td ::text").get(),
            'availability': table_rows[5].css("td ::text").re(r"In stock \((\d+) available\)"),
            # 'num_reviews': table_rows[6].css("td ::text").get(),
            'stars': book.css("p.star-rating").attrib['class'].re(r"star-rating (\w+)"),
            'category': book.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
            'price': book.css('p.price_color ::text').re(r"£([0-9]+\.[0-9]+)"),
            'description': book.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        }
