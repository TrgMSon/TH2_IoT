import time
from datetime import datetime
import pika


def run_producer():
    # Thông tin sinh viên theo yêu cầu đề bài
    ho_ten = "Lang Viet Thanh"
    ma_sv = "B23DCCN768"
    loi_chao = "Xin chao tu ung dung Python AMQP"

    # Kết nối tới RabbitMQ broker
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    queue_name = "iot_lab_queue"

    # Tạo hoặc sử dụng queue có tên: iot_lab_queue
    channel.queue_declare(queue=queue_name)

    print(
        f"[*] Ket noi thanh cong toi RabbitMQ broker (Queue: '{queue_name}').",
        flush=True,
    )
    print("[*] Bat dau gui message (nhan Ctrl+C de dung)...\n", flush=True)

    message_count = 1
    try:
        while True:
            # Nội dung message chứa: Lời chào - Mã SV - Họ tên SV
            message_body = f"{loi_chao} - {ma_sv} - {ho_ten}"

            # Gửi message vào queue
            channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=message_body.encode("utf-8"),
            )

            current_time = datetime.now().strftime("%H:%M:%S")
            print(
                f"[x] [{current_time}] Da gui message #{message_count}: {message_body}",
                flush=True,
            )

            message_count += 1
            # Gợi ý mở rộng: Cho phép producer gửi nhiều message liên tiếp (mỗi 3 giây)
            time.sleep(3)

    except KeyboardInterrupt:
        print("\n[!] Dung Producer.", flush=True)
    finally:
        connection.close()


if __name__ == "__main__":
    run_producer()
