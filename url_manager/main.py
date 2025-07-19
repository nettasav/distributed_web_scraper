import pymongo
from url_manager import *
import pika


def main():
    moongo_client = pymongo.MongoClient("mongodb://mongo:27017/")

    db = moongo_client["wikipedia_scraper"]
    unique_urls = db["unique_urls"]
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))

    channel = connection.channel()
    url_manager_obj = UrlManager(
        unique_urls, "check_duplicates", "urls_to_download", channel
    )

    url_manager_obj.start()

if __name__ == "__main__":
    main()
