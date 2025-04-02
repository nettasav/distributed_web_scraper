import pymongo
from url_manager import *
import pika


def main():

    # moongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    moongo_client = pymongo.MongoClient("mongodb://mongo:27017/")

    db = moongo_client["wikipedia_scraper"]
    unique_urls = db["unique_urls"]

    # connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))

    channel = connection.channel()
    # channel.queue_declare(queue="urls_to_download", durable=True)
    # channel.queue_declare(queue="check_duplicates", durable=True)
    url_manager_obj = UrlManager(
        unique_urls, "check_duplicates", "urls_to_download", channel
    )

    url_manager_obj.start()

    # my_url_manager = UrlManager(myclient)
    # my_url_manager.save_to_DB(ch=myclient, body={"www.hi"})
    # my_url_manager.start()


if __name__ == "__main__":
    main()
