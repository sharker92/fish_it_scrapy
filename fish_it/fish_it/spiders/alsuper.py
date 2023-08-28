from scrapy import Spider, Request
import re
from ..items import AlsuperItem
from scrapy.loader import ItemLoader
from scrapy.utils.defer import maybe_deferred_to_future

# https://api2.alsuper.com/v1/ms-products/branch/1000?page=5&limit=5000
# jala todos los productos y da más info. Es como la base de datos principal.
# https://api2.alsuper.com/v1/products/1152/branch/2
# la branch es el supermercado. Leones es el 6, el 1000 es el generico.
# sirve para obtener la info de un producto en especifico

PRODUCTS_PER_PAGE = 1


# Ver diferencia de productos entre tiendas.
class AlsuperSpider(Spider):
    name = "alsuper"
    allowed_domains = ["alsuper.com"]
    start_urls = [
        f"https://api2.alsuper.com/v1/ms-products/branch/1000?page=1&limit={PRODUCTS_PER_PAGE}"
    ]

    custom_settings = {
        "FEEDS": {"alsuperData.json": {"format": "json", "overwrite": True}}
    }

    async def parse(self, response):
        stores = await self.get_stores()
        try:
            products = response.json()["data"]["data"]
            for p in products:
                for s in stores:
                    il = ItemLoader(item=AlsuperItem(), selector=p)
                    il.add_value("ecommerce", p.get("ecommerce", None))
                    il.add_value("prod_id", p.get("id", None))
                    prod_id = p.get("id", None)
                    store_id = s.get("branch_id", None)

                    il.add_value("store_id", s.get("branch_id", None))
                    il.add_value("store_type", s.get("store_type", None))
                    il.add_value("plaza", s.get("plaza", None))
                    il.add_value("store_name", s.get("name", None))
                    il.add_value("geozone", s.get("geozone", None))
                    il.add_value("city", s.get("city", None))
                    il.add_value("address", s.get("address", None))
                    il.add_value("phone", s.get("phone", None))
                    il.add_value("email", s.get("email", None))
                    il.add_value("state", s.get("state", None))
                    il.add_value("store_ecommerce", s.get("ecommerce", None))

                    product_url = f"https://api2.alsuper.com/v1/products/{prod_id}/branch/{store_id}"
                    yield response.follow(
                        product_url,
                        meta={"il": il},
                        callback=self.parse_product_page,
                    )

            # page_number = re.search(r"(?<=page=)\d+", response.url).group()
            # next_page_number = int(page_number) + 1
            # relative_url = (
            #     f"1000?page={next_page_number}&limit={PRODUCTS_PER_PAGE}"
            # )
            # yield response.follow(relative_url, callback=self.parse)
        except KeyError:
            print("No se encontraron más articulos.")

    def parse_product_page(self, response):
        product = response.json()["data"]
        il = response.meta["il"]
        il.add_value("prod_name", product.get("name", None))
        il.add_value("image_url", product.get("image_url", None))
        il.add_value("unit", product.get("unit", None))
        il.add_value("weight", product.get("weight", None))
        il.add_value("packing", product.get("packing", None))
        il.add_value("variant", product.get("variant", None))
        il.add_value("madurity", product.get("madurity", None))
        il.add_value("share_url", product.get("share_url", None))
        il.add_value("ean", product.get("ean", None))
        il.add_value("restriction", product.get("restriction", None))
        il.add_value("offer_type", product.get("offer_type", None))
        il.add_value("smart_offer", product.get("smart_offer", None))
        il.add_value("promotion", product.get("promotion", None))
        il.add_value("regular_price", product.get("regular_price", None))
        il.add_value("price", product.get("price", None))
        il.add_value("stock", product.get("stock", None))
        yield il.load_item()

    async def get_stores(self):
        stores_url = "https://api2.alsuper.com/v1/stores?ecommerce=true"
        stores_request = Request(stores_url)
        deferred = self.crawler.engine.download(stores_request)
        stores_response = await maybe_deferred_to_future(deferred)
        stores = stores_response.json()["data"]
        general_store = {
            "branch_id": 1000,
            "store_type": "ALSUPER GENERAL",
            "ecommerce": True,
        }
        stores.insert(0, general_store)
        return stores
