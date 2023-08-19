# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# https://www.learndatasci.com/tutorials/using-databases-python-postgres-sqlalchemy-and-alembic/
from uuid import uuid4
from datetime import datetime
from itemadapter import ItemAdapter
from sqlalchemy import URL, DateTime, create_engine, ForeignKey, Column
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import (
    ARRAY,
    BOOLEAN,
    FLOAT,
    TEXT,
    INTEGER,
    UUID,
)

Base = declarative_base()


class FishItPipeline:
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline:
    def process_item(self, item, spider):
    # comparación de precio con producto anterior
        return item


class SaveToPostgreSQLPipeline:
    def __init__(self):
        url = URL.create(
            drivername="postgresql",
            username="fish_it",
            host="localhost",
            database="fish_it",
            port=5432,
            password="fish_it123",
        )
        self.engine = create_engine(url)
        self.recreate_database()
        # Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def process_item(self, item, spider):
        try:
            product = Alsuper(
                prod_id=item.get("prod_id", None),
                name=item.get("name", None),
                price=item.get("price", None),
                regular_price=item.get("regular_price", None),
                image_url=item.get("image_url", None),
                unit=item.get("unit", None),
                weight=item.get("weight", None),
                packing=item.get("packing", None),
                variant=item.get("variant", None),
                madurity=item.get("madurity", None),
                share_url=item.get("share_url", None),
                ean=item.get("ean", None),
                ecommerce=item.get("ecommerce", None),
            )
            self.session.add(product)
            self.session.commit()
            return item
        except Exception as error:
            print(error)

    def close_spider(self, spider):
        self.session.close()

    def recreate_database(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)


class Alsuper(Base):
    __tablename__ = "Alsuper"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    prod_id = Column(INTEGER)
    name = Column(TEXT)
    price = Column(FLOAT)
    regular_price = Column(FLOAT)
    image_url = Column(TEXT)
    unit = Column(TEXT)
    weight = Column(FLOAT)
    packing = Column(TEXT)
    variant = Column(TEXT)
    madurity = Column(ARRAY(TEXT))
    share_url = Column(TEXT)
    ean = Column(TEXT)
    ecommerce = Column(BOOLEAN)
    created_on = Column(DateTime(), default=datetime.now())
    updated_on = Column(
        DateTime(), default=datetime.now, onupdate=datetime.now()
    )

    def __repr__(self):
        return "<Alsuper(prod_id='{}', name='{}', price={}, share_url={})>".format(
            self.prod_id, self.name, self.price, self.share_url
        )
