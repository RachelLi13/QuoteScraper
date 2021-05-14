# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from re import M
from scrapy.item import Item, Field
from datetime import datetime
from scrapy.loader.processors import MapCompose, TakeFirst

#Removes unicode quotation marks 
def remove_quotes(text):
    text = text.strip(u'u2021c'u'\u201d')
    return text

def convert_date(text):
    #convert string date to Python Date
    return datetime.strptime(text, '%B %d, %Y')

def parse_location(text):
    # this simply removes "in" in country 
    return text[3:]

class QuoteItem(Item):
    quote_content = Field(
        input_processor = MapCompose(remove_quotes)
    )
    #What is pulled from the scraper
    quote_content = Field(
        input_processor=MapCompose(remove_quotes),
        #Takes first item out of the list
        output_processor=TakeFirst()
    )
    tags  = Field()
    author_name = Field(
        input_processor = MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    author_birthday = Field(
        input_processor=MapCompose(convert_date),
        output_processor=TakeFirst()
    )
    author_bornlocation = Field(
        input_processor=MapCompose(parse_location),
        output_processor=TakeFirst()        
    )
    author_bio = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()        
    )

    