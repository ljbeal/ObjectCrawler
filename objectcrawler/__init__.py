import logging

from objectcrawler.Crawler import SlotsCrawler

__all__ = ["SlotsCrawler"]

__version__ = "0.0.1"

logger = logging.getLogger(__name__)
logging.basicConfig(filename='crawler.log',
                    format="%(asctime)s %(levelname)-8s: %(message)s",
                    encoding='utf-8',
                    level=logging.DEBUG,
                    filemode="w")
