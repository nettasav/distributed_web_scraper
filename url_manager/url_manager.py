import pika

class UrlManager:
    def __init__(self, unique_urls, check_duplicates, urls_to_download, channel):
        self.unique_urls = unique_urls
        self.check_duplicates = check_duplicates
        self.urls_to_download = urls_to_download
        self.channel = channel

    def detect_duplicates(self, url):
        return self.unique_urls.find_one({"url": url})

    # def save_to_DB(self):
    #     pass

    def save_to_DB(self, ch, method, properties, body):
        """function to receive the message from rabbitmq
        print it
        sleep for 2 seconds
        ack the message"""

        print("received msg : ", body.decode("utf-8"))

        if not self.detect_duplicates(body):
            # if True:
            message = body
            self.channel.basic_publish(
                exchange="",
                routing_key=self.urls_to_download,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=pika.DeliveryMode.Persistent
                ),
            )
            print(f" [x] Sent {message}")
            data = {"url": str(body)}
            self.unique_urls.insert_one(data)

        # print("acking it")
        self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):

        self.channel.queue_declare(queue=self.check_duplicates, durable=True)
        self.channel.queue_declare(queue=self.urls_to_download, durable=True)

        print(" [*] Waiting for messages. To exit press CTRL+C")
        # seeding with initial url
        self.channel.basic_publish(
            exchange="",
            routing_key=self.check_duplicates,
            body="https://he.wikipedia.org/wiki/Evermore_(%D7%90%D7%9C%D7%91%D7%95%D7%9D)",
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=self.check_duplicates, on_message_callback=self.save_to_DB
        )

        self.channel.start_consuming()
