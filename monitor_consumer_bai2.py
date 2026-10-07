import json
import pika


def callback(ch, method, properties, body):
  try:
    data = json.loads(body.decode('utf-8'))

    device_id = data.get('device_id')
    temp = data.get('temperature')
    hum = data.get('humidity')
    sent_time = data.get('timestamp', 'N/A')

    # In thông tin nhận được kèm thời gian gửi
    print('=' * 35)
    print(f'Device:      {device_id}')
    print(f'Timestamp:   {sent_time}')
    print(f'Temperature: {temp} °C')
    print(f'Humidity:    {hum} %')

    # Kiểm tra các ngưỡng cảnh báo
    if temp is not None and temp > 35:
      print('>>> CANH BAO: Nhiet do cao!')

    if hum is not None and hum < 40:
      print('>>> CANH BAO: Do am thap!')

    # Xác nhận đã xử lý xong message
    ch.basic_ack(delivery_tag=method.delivery_tag)

  except Exception as e:
    print(f'Loi khi xu ly message: {e}')


def run_consumer():
  connection = pika.BlockingConnection(
      pika.ConnectionParameters(host='localhost')
  )
  channel = connection.channel()

  queue_name = 'sensor_data_queue'
  channel.queue_declare(queue=queue_name)

  channel.basic_consume(
      queue=queue_name, on_message_callback=callback, auto_ack=False
  )

  print(
      f"[*] Dang lang nghe tren queue '{queue_name}'. Nhan Ctrl+C de thoat."
  )
  try:
    channel.start_consuming()
  except KeyboardInterrupt:
    print('\n[!] Dung Monitoring Consumer.')
    channel.stop_consuming()
  finally:
    connection.close()


if __name__ == '__main__':
  run_consumer()