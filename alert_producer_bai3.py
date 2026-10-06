import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

EXCHANGE_NAME = 'iot_topic_exchange'

# Khai báo Topic Exchange
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic')

# Danh sách cảnh báo mô phỏng
alerts = [
    ("info", "Nhiet do phong may dang o muc 25C (Binh thuong)"),
    ("warning", "Nhiet do phong may vuot nguong warning (38C)"),
    ("critical", "Cam bien kho lanh mat ket noi critical")
]

for severity, message in alerts:
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=severity,
        body=message
    )
    print(f"[Producer] Da gui [{severity}]: '{message}'")

connection.close()