from html_parser import *
import pika


def main():

    # connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))

    channel = connection.channel()
    channel.queue_declare(queue="urls_to_download", durable=True)
    channel.queue_declare(queue="check_duplicates", durable=True)
    html_obj = HtmlParser("urls_to_download", "check_duplicates", channel, "./fs")

    html_obj.start()


if __name__ == "__main__":
    main()
