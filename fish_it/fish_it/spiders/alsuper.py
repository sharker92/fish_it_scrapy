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


class AlsuperSpider(scrapy.Spider):
    name = "alsuper"
    allowed_domains = ["alsuper.com"]
    start_urls = ["https://api2.alsuper.com/v1/ms-products/branch/1000?page=1&limit=15"]

    def parse(self, response):
        products = response.json()["data"]["data"]
        for p in products:
            il = ItemLoader(item=AlsuperItem(), selector=p)

            il.add_jmes("id", "id")
            il.add_jmes("name", "name")
            il.add_jmes("price", "price")
            il.add_jmes("image_url", "image_url")
            il.add_jmes("image_url", "image_url")
            il.add_jmes("weight", "weight")
            il.add_jmes("packing", "packing")
            il.add_jmes("variant", "variant")
            il.add_jmes("madurity", "madurity")
            yield {
                "id": p.get("id", None),
                "name": p.get("name", None),
                "price": p.get("price", None),
                "image_url": p.get("image_url", None),
                "unit": p.get("image_url", None),
                "weight": p.get("weight", None),
                "packing": p.get("packing", None),
                "variant": p.get("variant", None),
                "madurity": p.get("madurity", None),
            }
        page_number = re.search(r"(?<=page=)\d+", response.url).group()
        next_page_number = int(page_number) + 1
        relative_url = f"1000?page={next_page_number}&limit=15"
        if bool(len(next_page.json()["data"])):
            # next_page_url = response.urljoin(relative_url)
            yield response.follow(relative_url, callback=self.parse)


# {
# "data": {
# "code": "ERR_HTTP_INVALID_STATUS_CODE"
# }
# }
