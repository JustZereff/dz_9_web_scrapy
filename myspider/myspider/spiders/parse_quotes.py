import scrapy

class ParseQuotesSpider(scrapy.Spider):
    name = "parse_quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        raw_quotes = response.xpath('//div[@class="quote"]')
        
        # парсимо сторінку
        for r_quote in raw_quotes:
            quote = r_quote.xpath('.//span[@class="text"]/text()').get(default='')
            author = r_quote.xpath('.//small[@class="author"]/text()').get(default='')
            tags = r_quote.xpath('.//a[@class="tag"]/text()').extract()
            yield {
                'quote': quote,
                'author': author,
                'tags': tags
            }
        
        # Переходими на іншу сторінку, якщо вона існує
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
