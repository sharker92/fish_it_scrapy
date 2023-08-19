import scrapy
import re
from ..items import AlsuperItem
from scrapy.loader import ItemLoader

# https://api2.alsuper.com/v1/ms-products/branch/1000?page=5&limit=5000
# jala todos los productos y da más info. Es como la base de datos principal.
# https://api2.alsuper.com/v1/products/1152/branch/2
# la branch es el supermercado. Leones es el 6, el 1000 es el generico.
# sirve para obtener la info de un producto en especifico

PRODUCTS_PER_PAGE = 1


class AlsuperSpider(scrapy.Spider):
    name = "alsuper"
    allowed_domains = ["alsuper.com"]
    start_urls = [
        f"https://api2.alsuper.com/v1/ms-products/branch/1000?page=1&limit={PRODUCTS_PER_PAGE}"
    ]

    custom_settings = {
        "FEEDS": {"alsuperData.json": {"format": "json", "overwrite": True}}
    }

    def parse(self, response):
        try:
            products = response.json()["data"]["data"]
            for p in products:
                il = ItemLoader(item=AlsuperItem(), selector=p)
                il.add_value("ecommerce", p.get("ecommerce", None))
                product_id = p.get("id", None)
                product_url = f"https://api2.alsuper.com/v1/products/{product_id}/branch/1000"
                yield response.follow(
                    product_url,
                    meta={"il": il},
                    callback=self.parse_product_page,
                )

            page_number = re.search(r"(?<=page=)\d+", response.url).group()
            next_page_number = int(page_number) + 1
            relative_url = (
                f"1000?page={next_page_number}&limit={PRODUCTS_PER_PAGE}"
            )
            yield response.follow(relative_url, callback=self.parse)
        except KeyError:
            print("No se encontraron más articulos.")

    def parse_product_page(self, response):
        product = response.json()["data"]
        il = response.meta["il"]
        il.add_value("prod_id", product.get("id", None))
        il.add_value("name", product.get("name", None))
        il.add_value("price", product.get("price", None))
        il.add_value("regular_price", product.get("regular_price", None))
        il.add_value("image_url", product.get("image_url", None))
        il.add_value("unit", product.get("unit", None))
        il.add_value("weight", product.get("weight", None))
        il.add_value("packing", product.get("packing", None))
        il.add_value("variant", product.get("variant", None))
        il.add_value("madurity", product.get("madurity", None))
        il.add_value("share_url", product.get("share_url", None))
        il.add_value("ean", product.get("ean", None))
        yield il.load_item()
