# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


class AlsuperItem(scrapy.Item):
    id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    image_url = scrapy.Field(output_processor=TakeFirst())
    unit = scrapy.Field(output_processor=TakeFirst())
    weight = scrapy.Field(output_processor=TakeFirst())
    packing = scrapy.Field(output_processor=TakeFirst())
    variant = scrapy.Field(output_processor=TakeFirst())
    madurity = scrapy.Field()
    share_url = scrapy.Field(output_processor=TakeFirst())
    ean = scrapy.Field(output_processor=TakeFirst())
    ecommerce = scrapy.Field(output_processor=TakeFirst())
    regular_price = scrapy.Field(output_processor=TakeFirst())
