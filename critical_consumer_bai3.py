import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

EXCHANGE_NAME = 'iot_topic_exchange'
QUEUE_NAME = 'critical_queue'
LOG_FILE = 'alerts.log'

# Khai báo Topic Exchange và Queue
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic')
channel.queue_declare(queue=QUEUE_NAME, durable=True)

# Bind 1: Nhận mức 'critical'
channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key='critical')

# Bind 2: Sử dụng pattern '#' để nhận TẤT CẢ các mức cảnh báo
channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key='#')

def callback(ch, method, properties, body):
    severity = method.routing_key
    msg_content = body.decode()
    log_line = f"[{severity.upper()}] {msg_content}\n"
    
    # In ra console
    print(f"[critical_queue] Da nhan: {msg_content}")
    
    # Ghi nối tiếp vào file log
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_line)

channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

print(f"[*] Dang cho va ghi LOG vao '{LOG_FILE}'. Nhan Ctrl+C de thoat.")
channel.start_consuming()