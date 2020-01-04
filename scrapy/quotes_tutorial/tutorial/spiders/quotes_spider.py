import scrapy


class QuotesSpider(scrapy.Spider):
    # Name of the spider
    name = "quotes"

    # URL's to scrape
    start_urls = [
        'http://quotes.toscrape.com/page/1/'
    ]

    def parse(self, response):
        # Extract the quote, author, and tags for each quote entry
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        # Follow the next link if available
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
