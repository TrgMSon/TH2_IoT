import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

EXCHANGE_NAME = 'iot_topic_exchange'
QUEUE_NAME = 'warning_queue'

# Khai báo Topic Exchange và Queue
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic')
channel.queue_declare(queue=QUEUE_NAME, durable=True)

# Bind queue nhận riêng mức 'warning'
channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key='warning')

def callback(ch, method, properties, body):
    print(f"[warning_queue] Da nhan: {body.decode()}")

channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

print("[*] Dang cho canh bao WARNING. Nhan Ctrl+C de thoat.")
channel.start_consuming()