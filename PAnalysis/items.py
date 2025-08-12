# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PanalysisItem(scrapy.Item):
    price = scrapy.Field()
    property_type = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    floor_area = scrapy.Field()
    price_per_area = scrapy.Field()
    
    pass
