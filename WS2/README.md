# 🌍 AI Travel Planner & Trip Tracker

Ứng dụng **AI Travel Planner** cho phép bạn:
- Lên kế hoạch chi tiết cho chuyến đi (lịch trình, ngân sách, hoạt động)
- Gợi ý điểm đến, món ăn, văn hóa, sự kiện tại các địa điểm
- Theo dõi tiến độ chuyến đi và so sánh với kế hoạch ban đầu
- Lưu và quản lý nhiều cuộc hội thoại lập kế hoạch khác nhau

---

## 📦 1. Yêu cầu hệ thống

- Python >= 3.9
- [pip](https://pip.pypa.io/en/stable/)
- Tài khoản **Azure OpenAI** và đã tạo model `gpt-4o-mini`
- File `.env` chứa thông tin API:
  ```
  AZURE_OPENAI_ENDPOINT=<endpoint của bạn>
  AZURE_OPENAI_API_KEY=<API key của bạn>
  ```

---

## ⚙️ 2. Cài đặt

1. **Clone project**
   ```bash
   git clone <link-repo>
   cd <tên-thư-mục>
   ```

2. **Tạo môi trường ảo**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Cài đặt thư viện**
   ```bash
   pip install -r requirements.txt
   ```

4. **Tạo file `.env`**
   ```bash
   AZURE_OPENAI_ENDPOINT=...
   AZURE_OPENAI_API_KEY=...
   ```

---

## 🚀 3. Chạy ứng dụng

```bash
streamlit run app.py
```

Sau khi chạy, ứng dụng sẽ mở trên trình duyệt tại địa chỉ:
```
http://localhost:8501
```

---

## 💡 4. Cách sử dụng

### 4.1 Chatbot (Tab **💬 Chatbot**)
- Gõ yêu cầu: *"Lên kế hoạch đi Hà Nội 3 ngày 2 đêm"*
- Bot sẽ gợi ý lịch trình chi tiết, ngân sách, hoạt động
- Bạn có thể hỏi thêm: *"Ở Hà Nội có gì?"*, *"Món ăn đặc sản ở Hội An"*

### 4.2 Theo dõi chuyến đi (Tab **📍 Tracking**)
- Nhập **Ngày**, **Hoạt động đã hoàn thành**, **Chi tiêu hôm nay**
- Bấm **Cập nhật tiến độ**
- Chọn **So sánh với kế hoạch** để xem bạn có đang theo đúng ngân sách & tiến độ không

### 4.3 Quản lý nhiều kế hoạch
- Dùng menu bên trái để chọn cuộc hội thoại
- Bấm **➕ New Conversation** để tạo kế hoạch mới
- Bấm **♻️ Reset Current Conversation** để làm mới hội thoại hiện tại

---

## 📂 5. Cấu trúc thư mục

```
.
├── app.py              # File chạy chính với Streamlit
├── utils.py            # Hàm xử lý AI, lưu dữ liệu, so sánh tiến độ
├── prompts.py          # System prompt cho AI
├── conversations.json  # Lưu toàn bộ hội thoại và tiến độ
├── requirements.txt    # Thư viện cần cài
└── README.md           # Hướng dẫn sử dụng
```

---

## ✨ 6. Tính năng chính
- Lên kế hoạch chi tiết
- Gợi ý địa điểm, món ăn, hoạt động
- Theo dõi & so sánh tiến độ chuyến đi
- Lưu nhiều kế hoạch khác nhau
- Hỗ trợ tiếng Việt và tiếng Anh

---

## 📌 Lưu ý
- Bot **chỉ trả lời các câu hỏi liên quan đến du lịch, điểm đến, chuyến đi**
- Nếu câu hỏi không liên quan, bot sẽ từ chối trả lời
