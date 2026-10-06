# THỰC HÀNH: LẬP TRÌNH PYTHON VỚI GIAO THỨC AMQP

Dự án này minh họa cách sử dụng RabbitMQ làm Message Broker để truyền tải và xử lý các thông điệp cảnh báo (`warning`, `critical`) giữa Producer và các Consumer thông qua giao thức AMQP trong Python.

---

## 1. Broker Sử Dụng

- **Message Broker:** [RabbitMQ](https://www.rabbitmq.com/)
- **Management Plugin:** `rabbitmq_management` (Giao diện quản trị Web tại `http://localhost:15672`)
- **Giao thức:** AMQP 0-9-1 (cổng kết nối mặc định `5672`)

---

## 2. Hướng Dẫn Chạy Chương Trình

### Bước 1: Khởi động dịch vụ RabbitMQ

1. Mở **Command Prompt (CMD)** với quyền quản trị (**Run as Administrator**).
2. Di chuyển đến thư mục `sbin` của `rabbitmq_server`:
   ```cmd
   cd "D:\RabbitMQ_server\rabbitmq_server-4.3.6\sbin"