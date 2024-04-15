"""
Toplevel __init__ providing all tools and logger
"""

import logging

from objectcrawler.crawler import Crawler

__all__ = ["Crawler"]

__version__ = "0.0.2"

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="crawler.log",
    format="%(asctime)s %(levelname)-8s: %(message)s",
    encoding="utf-8",
    level=logging.DEBUG,
    filemode="w",
)
