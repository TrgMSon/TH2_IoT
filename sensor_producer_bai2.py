from datetime import datetime
import json
import random
import time
import pika


def run_producer():
  # Kết nối tới RabbitMQ broker
  connection = pika.BlockingConnection(
      pika.ConnectionParameters(host='localhost')
  )
  channel = connection.channel()

  queue_name = 'sensor_data_queue'
  channel.queue_declare(queue=queue_name)

  # Danh sách 3 cảm biến mô phỏng
  devices = ['sensor01', 'sensor02', 'sensor03']

  print(
      f"[*] Bat dau mo phong {len(devices)} cam bien gui du lieu moi 3 giay..."
  )
  print('[*] Nhan Ctrl+C de dung.\n')

  try:
    while True:
      # Lựa chọn ngẫu nhiên một cảm biến trong 3 cảm biến để gửi dữ liệu
      device_id = random.choice(devices)

      # Đóng gói dữ liệu kèm thời gian gửi (định dạng YYYY-MM-DD HH:MM:SS)
      payload = {
          'device_id': device_id,
          'temperature': round(random.uniform(20.0, 45.0), 1),
          'humidity': round(random.uniform(20.0, 80.0), 1),
          'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
      }

      message_body = json.dumps(payload)
      channel.basic_publish(
          exchange='', routing_key=queue_name, body=message_body
      )

      print(f'[x] Da gui tu [{device_id}]: {message_body}')
      time.sleep(3)

  except KeyboardInterrupt:
    print('\n[!] Dung Sensor Producer.')
  finally:
    connection.close()


if __name__ == '__main__':
  run_producer()