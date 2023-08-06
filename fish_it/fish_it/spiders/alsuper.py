import scrapy
import re
from ..items import AlsuperItem
from scrapy.loader import ItemLoader

# https://api2.alsuper.com/v1/ms-products/branch/1000?page=5&limit=5000
# jala todos los productos y da más info. Es como la base de datos principal.
# https://api2.alsuper.com/v1/products/1152/branch/2 El branch no tiene sentido?!
# normalmente usan el 6 -> del 1 al 9 y la 1000
# sirve para obtener la info de un producto en especifico
# la branch es el super. Leones es el 6.

PRODUCTS_PER_PAGE = 5000


class AlsuperSpider(scrapy.Spider):
    name = "alsuper"
    allowed_domains = ["alsuper.com"]
    start_urls = [
        f"https://api2.alsuper.com/v1/ms-products/branch/1000?page=1&limit={PRODUCTS_PER_PAGE}"
    ]

    def parse(self, response):
        try:
            products = response.json()["data"]["data"]
            for p in products:
                il = ItemLoader(item=AlsuperItem(), selector=p)
                il.add_value("id", p.get("id", None))
                il.add_value("name", p.get("name", None))
                il.add_value("price", p.get("price", None))
                il.add_value("image_url", p.get("image_url", None))
                il.add_value("unit", p.get("unit", None))
                il.add_value("weight", p.get("weight", None))
                il.add_value("packing", p.get("packing", None))
                il.add_value("variant", p.get("variant", None))
                il.add_value("madurity", p.get("madurity", None))
                il.add_value("share_url", p.get("share_url", None))
                yield il.load_item()
            # yield from products

            page_number = re.search(r"(?<=page=)\d+", response.url).group()
            next_page_number = int(page_number) + 1
            relative_url = f"1000?page={next_page_number}&limit={PRODUCTS_PER_PAGE}"
            yield response.follow(relative_url, callback=self.parse)
        except KeyError:
            print('No se encontraron más articulos.')


# {
# "data": {
# "code": "ERR_HTTP_INVALID_STATUS_CODE"
# }
# }
