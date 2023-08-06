# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


class AlsuperItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()
    unit = scrapy.Field()
    weight = scrapy.Field()
    packing = scrapy.Field()
    variant = scrapy.Field()
    madurity = scrapy.Field()
    share_url = scrapy.Field()
