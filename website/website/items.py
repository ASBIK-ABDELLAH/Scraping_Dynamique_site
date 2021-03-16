# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BroschItem(scrapy.Item):
    url_name = scrapy.Field()
    Preis = scrapy.Field()
    Stuck = scrapy.Field()
    inkl = scrapy.Field()
    Lifertermin = scrapy.Field()
    Ausfuhrung = scrapy.Field()
    name = scrapy.Field()



