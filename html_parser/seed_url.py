import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="urls_to_download", durable=True)

message = "https://en.wikipedia.org/wiki/Parsing"
channel.basic_publish(
    exchange="",
    routing_key="urls_to_download",
    body=message,
    properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
)
print(f" [x] Sent {message}")
connection.close()
