# THỰC HÀNH: LẬP TRÌNH PYTHON VỚI GIAO THỨC AMQP

## Broker Sử Dụng

- **Message Broker:** [RabbitMQ](https://www.rabbitmq.com/)
- **Management Plugin:** `rabbitmq_management` (Giao diện quản trị Web tại `http://localhost:15672`)
- **Giao thức:** AMQP 0-9-1 (cổng kết nối mặc định `5672`)

---

## Bài 3. Mô phỏng hệ thống điều phối cảnh báo IoT với exchange

### 1. Giới thiệu
Làm quen với exchange và routing key trong AMQP.
- **`alert_producer_bai3.py`**: là nguồn phát dữ liệu, gửi các thông điệp cảnh báo đến RabbitMQ Exchange.
- **`warning_consumer_bai3.py`**: là dịch vụ lắng nghe và tiếp nhận riêng các cảnh báo mức warning để ghi log theo dõi.
- **`critical_consumer_bai3.py`**: là dịch vụ lắng nghe và tiếp nhận riêng các cảnh báo mức critical để ghi log theo dõi.

### 2. Cách chạy chương trình

### Bước 1: Khởi động dịch vụ RabbitMQ

1. Mở **Command Prompt (CMD)** với quyền quản trị (**Run as Administrator**).
2. Di chuyển đến thư mục `sbin` của `rabbitmq_server`:
```cmd
   cd "D:\RabbitMQ_server\rabbitmq_server-4.3.6\sbin"
```
3. Chạy lần lượt 2 lệnh sau để bật plugin quản lý và khởi chạy dịch vụ:
```
rabbitmq-plugins.bat enable rabbitmq_management
rabbitmq-service.bat start
```
4. Kiểm tra dịch vụ đã hoạt động hay chưa bằng cách kiểm tra cổng 15672:
```
netstat -ano | findstr 15672
```
*Nếu kết quả hiển thị dòng trạng thái LISTENING tại cổng 15672, RabbitMQ đã khởi động thành công.*
*Nếu không có kết quả thì dừng dịch vụ RabbitMQ, dùng lệnh sau:*
```
rabbitmq-service.bat stop
```
*Sau đó tiếp tục làm theo từ bước 3.*

### Bước 2: Chạy các chương trình
Sau khi RabbitMQ khởi động thành công, mở 3 cửa sổ Terminal/CMD riêng biệt và tiến hành chạy lần lượt 3 file theo thứ tự:

**Khởi chạy Warning Consumer:**
```
python warning_consumer_bai3.py
```

**Khởi chạy Critical Consumer:**
```
python critical_consumer_bai3.py
```

**Khởi chạy Alert Producer (để phát tin nhắn):**
```
python alert_producer_bai3.py
```

### 3. kết quả đạt được
**warning_consumer_bai3.py**
```
[*] Dang cho canh bao WARNING. Nhan Ctrl+C de thoat.
[warning_queue] Da nhan: Nhiet do phong may vuot nguong warning (38C)
```

**critical_consumer_bai3.py**
```
[*] Dang cho va ghi LOG vao 'alerts.log'. Nhan Ctrl+C de thoat.
[critical_queue] Da nhan: Nhiet do phong may dang o muc 25C (Binh thuong)
[critical_queue] Da nhan: Nhiet do phong may vuot nguong warning (38C)
[critical_queue] Da nhan: Cam bien kho lanh mat ket noi critical
```

**alert_producer_bai3.py**
```
[Producer] Da gui [info]: 'Nhiet do phong may dang o muc 25C (Binh thuong)'
[Producer] Da gui [warning]: 'Nhiet do phong may vuot nguong warning (38C)'
[Producer] Da gui [critical]: 'Cam bien kho lanh mat ket noi critical'
```