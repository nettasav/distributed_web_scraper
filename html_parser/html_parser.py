from bs4 import BeautifulSoup

import requests
import pika

from urllib.parse import unquote

# import os
# urllib.parse.unqouate


class HtmlParser:

    wiki_prefix = "https://he.wikipedia.org"
    wiki_folder = "/wiki/"

    def __init__(
        self,
        urls_to_download,
        check_duplicates,
        channel,
        output_path,
        urls_to_parse_queue=None,
    ):
        self.urls_to_download = urls_to_download
        self.urls_to_parse_queue = urls_to_parse_queue
        self.check_duplicates = check_duplicates
        self.channel = channel
        self.output_path = output_path

    def get_html(self, url):
        try:
            html = requests.get(url)
            return html.content
        except:
            return

    def extract_urls(self, html):
        soup = BeautifulSoup(html, "html.parser")
        links = [
            self.wiki_prefix + link.get("href")
            for link in soup.find_all("a")
            if link.get("href", "").startswith(self.wiki_folder)
            and ":" not in link.get("href", "")[len(self.wiki_folder) :]
        ]
        return links

    def save_to_fs(self, name, html):
        with open(f"{self.output_path}/{unquote(name)}.html", "w") as file:
            file.write(html.decode())

    def process_url(self, channel, method, properties, body):
        # body = url
        decoded_body = body.decode()
        print(f" [x] Received {decoded_body}")
        html = self.get_html(decoded_body)
        if html:
            links = self.extract_urls(html)
            name = decoded_body[
                len(self.wiki_prefix) + len(self.wiki_folder) :
            ].replace("/", "_")

            self.save_to_fs(name, html)

            for link in links:
                channel.basic_publish(
                    exchange="",
                    routing_key=self.check_duplicates,
                    body=link,
                    properties=pika.BasicProperties(
                        delivery_mode=pika.DeliveryMode.Persistent
                    ),
                )
                print(f" [x] Sent {link}")
        self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):

        # os.mkdir(self.output_path)

        self.channel.queue_declare(queue=self.urls_to_download, durable=True)
        self.channel.queue_declare(queue=self.check_duplicates, durable=True)

        print(" [*] Waiting for messages. To exit press CTRL+C")

        self.channel.basic_qos(prefetch_count=1)

        self.channel.basic_consume(
            queue=self.urls_to_download, on_message_callback=self.process_url
        )

        self.channel.start_consuming()


# test_html_obj = HtmlParser(None, None, None, "./fs")

# my_html = {"bla": "bla"}
# url = "https://he.wikipedia.org/wiki/Docker/bla"
# name = url[len(test_html_obj.wiki_prefix) + len(test_html_obj.wiki_folder) :].replace(
#     "/", "_"
# )
# print(name)
# test_html_obj.save_to_fs(name, my_html)
# # # test_html_obj.get_html("https://en.wikipedia.org/wiki/Parsing")
# test_html_obj.get_html("https://he.wikipedia.org/wiki/Docker")
# print(test_html_obj.html.text)
# # test_html_obj.extract_urls()
# # print(test_html_obj.links)
