import scrapy


class ParseAuthorSpider(scrapy.Spider):
    name = "parse_author"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        raw_quotes = response.xpath('//div[@class="quote"]')
        
        # парсимо сторінку
        for author_links in raw_quotes:
            author_links = response.xpath('.//a[contains(@href, "/author/")]/@href').extract()
            for link in author_links:
                yield response.follow(link, callback=self.parse_author_page)
        
        # Переходими на іншу сторінку, якщо вона існує
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_author_page(self, response):
        fullname = response.xpath('//h3[@class="author-title"]/text()').get(default='')
        born_date = response.xpath('//span[@class="author-born-date"]/text()').get(default='')
        born_location = response.xpath('//span[@class="author-born-location"]/text()').get(default='')
        raw_description = response.xpath('//div[@class="author-description"]/text()').get(default='')
        description = raw_description.replace("\n", "").strip()
        yield {
            'fullname': fullname,
            'born_date': born_date,
            'born_location': born_location,
            'description': description
        }