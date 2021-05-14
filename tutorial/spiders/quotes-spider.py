import scrapy
from scrapy.loader import ItemLoader
from tutorial.items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
            #Pulling the all the quotes from a page 
            quotes = response.css('div.quote')
            for quote in quotes:
                # yield {
                #     'text': quote.css('.text::text').get(),
                #     'author': quote.css('.author::text').get(),
                #     'tags': quote.css('.tag::text').getall(),
                # }
                #Use ItemLoader bc it allows for pre/post processing 
                loader = ItemLoader(item = QuoteItem(), selector = quote)
                #pulling quote content and tags
                loader.add_css('quote_content','.text::text')
                loader.add_css('tags', '.tag::text')
                quote_item = loader.load_item()

                #Using shortcuts, searches for all author info links and calls parse_author on them
                author_page = quote.css('.quote span a')
                yield from response.follow_all(author_page, callback = self.parse_author, meta={'quote_item': quote_item})

            #searches for all next links and recalls this function to parse for all quotes
            pagination_links = response.css('.next a')
            yield from response.follow_all(pagination_links, callback = self.parse)

    
    #parsing the author page for information
    def parse_author(self, response):
        quote_item = response.meta['quote_item']
        loader = ItemLoader(item=quote_item, response=response)
        loader.add_css('author_name', '.author-title::text')
        loader.add_css('author_birthday', '.author-born-date::text')
        loader.add_css('author_bornlocation', '.author-born-location::text')
        loader.add_css('author_bio', '.author-description::text')
        yield loader.load_item()

