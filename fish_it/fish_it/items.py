# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def serialize_smart_offer(value):
    return float(value)


class AlsuperItem(scrapy.Item):
    # Stores
    store_id = scrapy.Field(output_processor=TakeFirst())
    store_type = scrapy.Field(output_processor=TakeFirst())
    plaza = scrapy.Field(output_processor=TakeFirst())
    store_name = scrapy.Field(output_processor=TakeFirst())
    geozone = scrapy.Field(output_processor=TakeFirst())
    city = scrapy.Field(output_processor=TakeFirst())
    address = scrapy.Field(output_processor=TakeFirst())
    phone = scrapy.Field(output_processor=TakeFirst())
    email = scrapy.Field(output_processor=TakeFirst())
    state = scrapy.Field(output_processor=TakeFirst())
    store_ecommerce = scrapy.Field(output_processor=TakeFirst())
    delivery = scrapy.Field(output_processor=TakeFirst())
    # products
    prod_id = scrapy.Field(output_processor=TakeFirst())
    ecommerce = scrapy.Field(output_processor=TakeFirst())
    # product
    prod_name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    regular_price = scrapy.Field(output_processor=TakeFirst())
    image_url = scrapy.Field(output_processor=TakeFirst())
    unit = scrapy.Field(output_processor=TakeFirst())
    weight = scrapy.Field(output_processor=TakeFirst())
    packing = scrapy.Field(output_processor=TakeFirst())
    variant = scrapy.Field(output_processor=TakeFirst())
    madurity = scrapy.Field()
    share_url = scrapy.Field(output_processor=TakeFirst())
    ean = scrapy.Field(output_processor=TakeFirst())
    restriction = scrapy.Field(output_processor=TakeFirst())
    offer_type = scrapy.Field(output_processor=TakeFirst())
    stock = scrapy.Field(output_processor=TakeFirst())
    promotion = scrapy.Field(output_processor=TakeFirst())
    smart_offer = scrapy.Field(
        serializer=serialize_smart_offer, output_processor=TakeFirst()
    )
