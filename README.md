# THỰC HÀNH: LẬP TRÌNH PYTHON VỚI GIAO THỨC AMQP

## Broker Sử Dụng

- **Message Broker:** [RabbitMQ](https://www.rabbitmq.com/)
- **Management Plugin:** `rabbitmq_management` (Giao diện quản trị Web tại `http://localhost:15672`)
- **Giao thức:** AMQP 0-9-1 (cổng kết nối mặc định `5672`)

---

## Bài 1. Gửi và nhận message cơ bản qua queue

### 1. Giới thiệu
Làm quen với mô hình producer → queue → consumer trong AMQP.
- **`producer_bai1.py`**: kết nối tới RabbitMQ broker và gửi các message chứa thông tin sinh viên vào queue `iot_lab_queue`.
- **`consumer_bai1.py`**: lắng nghe queue `iot_lab_queue`, tiếp nhận message và in ra nội dung cùng thời điểm nhận.

### 2. Cách chạy chương trình
Sau khi RabbitMQ khởi động thành công, mở 2 cửa sổ Terminal/CMD riêng biệt và tiến hành chạy lần lượt 2 file theo thứ tự:

**Khởi chạy Consumer (lắng nghe trước):**
```cmd
python consumer_bai1.py
```

**Khởi chạy Producer (để phát message):**
```cmd
python producer_bai1.py
```

### 3. Kết quả đạt được

**producer_bai1.py**
```text
[*] Ket noi thanh cong toi RabbitMQ broker (Queue: 'iot_lab_queue').
[*] Bat dau gui message (nhan Ctrl+C de dung)...

[x] [13:30:11] Da gui message #1: Xin chao tu ung dung Python AMQP - B23DCCN768 - Lang Viet Thanh
[x] [13:30:14] Da gui message #2: Xin chao tu ung dung Python AMQP - B23DCCN768 - Lang Viet Thanh
[x] [13:30:17] Da gui message #3: Xin chao tu ung dung Python AMQP - B23DCCN768 - Lang Viet Thanh
```

**consumer_bai1.py**
```text
[*] Dang lang nghe tren queue 'iot_lab_queue'. Nhan Ctrl+C de thoat.

Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN768 - Lang Viet Thanh
Thoi gian nhan: 13:30:11
--------------------------------------------------
Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN768 - Lang Viet Thanh
Thoi gian nhan: 13:30:14
--------------------------------------------------
Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN768 - Lang Viet Thanh
Thoi gian nhan: 13:30:17
--------------------------------------------------
```

---

## Bài 2. Mô phỏng cảm biến IoT gửi dữ liệu môi trường

### 1. Giới thiệu
Mô phỏng thiết bị IoT gửi telemetry qua AMQP.
- **`sensor_producer_bai2.py`**: là cảm biến gửi dữ liệu nhiệt độ, độ ẩm mỗi 3 giây.
- **`monitor_consumer_bai2.py`**: là dịch vụ lắng nghe, tiếp nhận dữ liệu từ sensor và in ra thông tin nhận được và cảnh báo (nếu có).

### 2. Cách chạy chương trình

### Bước 1: Khởi động dịch vụ RabbitMQ

Mở **Command Prompt (CMD)**
```cmd
   docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```
Xác minh container đang chạy:
```
docker ps
```
*Nếu thấy container rabbitmq có trạng thái Up, dịch vụ đã sẵn sàng hoạt động.*

**Nếu chưa có docker thì cài đặt [Docker](https://www.docker.com/products/docker-desktop/)**

### Bước 2: Chạy các chương trình
Sau khi RabbitMQ khởi động thành công, mở 2 cửa sổ Terminal/CMD riêng biệt và tiến hành chạy lần lượt 2 file theo thứ tự:

**Khởi chạy Monitor Consumer:**
```
python monitor_consumer_bai2.py
```

**Khởi chạy Sensor Producer:**
```
python sensor_producer_bai2.py
```

### 3. kết quả đạt được

**sensor_producer_bai2.py**
```
[x] Da gui tu [sensor03]: {"device_id": "sensor03", "temperature": 22.6, "humidity": 72.0, "timestamp": "2026-10-07 10:22:05"}
[x] Da gui tu [sensor01]: {"device_id": "sensor01", "temperature": 43.0, "humidity": 69.9, "timestamp": "2026-10-07 10:22:08"}
[x] Da gui tu [sensor02]: {"device_id": "sensor02", "temperature": 36.9, "humidity": 23.0, "timestamp": "2026-10-07 10:22:11"}
```
**monitor_consumer_bai3.py**
```
===================================
Device:      sensor03
Timestamp:   2026-10-07 10:22:05
Temperature: 22.6 °C
Humidity:    72.0 %
===================================
Device:      sensor01
Timestamp:   2026-10-07 10:22:08
Temperature: 43.0 °C
Humidity:    69.9 %
>>> CANH BAO: Nhiet do cao!
===================================
Device:      sensor02
Timestamp:   2026-10-07 10:22:11
Temperature: 36.9 °C
Humidity:    23.0 %
>>> CANH BAO: Nhiet do cao!
>>> CANH BAO: Do am thap!
```

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