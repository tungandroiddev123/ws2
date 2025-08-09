import os
import json
from typing import Dict, List
from openai import AzureOpenAI
from dotenv import load_dotenv
import uuid

load_dotenv()

DATA_FILE = "conversations.json"

client = AzureOpenAI(
    api_version="2024-07-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

# ===== JSON FILE HANDLING =====
def load_conversations():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_conversations(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ===== CONVERSATION HANDLING =====
def get_user_conversation(user_id, conv_id):
    data = load_conversations()
    conv = data.get(user_id, {}).get(conv_id)

    # ✅ Auto-fix dữ liệu cũ nếu là list
    if isinstance(conv, list):
        conv = {"messages": conv, "trip_progress": []}
    elif not isinstance(conv, dict):
        conv = {"messages": [], "trip_progress": []}

    return conv

def save_user_conversation(user_id, conv_id, conversation):
    data = load_conversations()
    if user_id not in data:
        data[user_id] = {}
    if conv_id not in data[user_id]:
        data[user_id][conv_id] = {"messages": [], "trip_progress": []}

    data[user_id][conv_id]["messages"] = conversation
    save_conversations(data)

def create_new_conversation(user_id):
    conv_id = str(uuid.uuid4())
    data = load_conversations()
    if user_id not in data:
        data[user_id] = {}
    data[user_id][conv_id] = {"messages": [], "trip_progress": []}
    save_conversations(data)
    return conv_id

def list_conversations(user_id: str) -> List[str]:
    return list(load_conversations().get(user_id, {}).keys())

# ===== AI CHAT (CHUYÊN VỀ TRIP) =====
TRIP_ONLY_SYSTEM_PROMPT = """
Bạn là một trợ lý AI chuyên về du lịch và quản lý chuyến đi.
Nhiệm vụ:
- Lập kế hoạch chuyến đi (lịch trình, ngân sách, phương tiện, hoạt động)
- Gợi ý thông tin về điểm đến, ẩm thực, văn hóa, thời tiết, sự kiện
- Theo dõi tiến độ chuyến đi và so sánh với kế hoạch
- Trả lời các câu hỏi khám phá như: "Ở [địa điểm] có gì?", "Nên đi đâu ở [địa điểm]?"

Nguyên tắc:
- Nếu câu hỏi KHÔNG liên quan tới du lịch, địa điểm, chuyến đi hoặc các hoạt động liên quan, hãy trả lời:
"Xin lỗi, tôi chỉ hỗ trợ các câu hỏi liên quan đến chuyến đi và lập kế hoạch du lịch."
- Ngôn ngữ mặc định: Tiếng Việt (trừ khi người dùng yêu cầu ngôn ngữ khác)
"""

def chat_with_ai(conversation_history: List[Dict]) -> str:
    # Đưa system prompt lên đầu để giới hạn phạm vi trả lời
    messages = [{"role": "system", "content": TRIP_ONLY_SYSTEM_PROMPT}]
    messages.extend(conversation_history)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content

def generate_plan(conversation_history):
    messages = [{"role": "system", "content": TRIP_ONLY_SYSTEM_PROMPT}]
    messages.extend(conversation_history)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content

# ===== TRIP PROGRESS =====
def update_trip_progress(user_id, conv_id, day, completed, spent):
    data = load_conversations()
    conv = data.get(user_id, {}).get(conv_id)

    if isinstance(conv, list):
        conv = {"messages": conv, "trip_progress": []}
        data[user_id][conv_id] = conv
    elif not isinstance(conv, dict):
        conv = {"messages": [], "trip_progress": []}
        data[user_id][conv_id] = conv

    conv.setdefault("trip_progress", []).append({
        "day": day,
        "completed": completed,
        "spent": spent
    })

    save_conversations(data)

def compare_with_plan(user_id, conv_id):
    conv = get_user_conversation(user_id, conv_id)
    plan = conv.get("plan", {})
    progress = conv.get("trip_progress", [])

    if not plan:
        return "⚠️ Chưa có kế hoạch để so sánh."

    total_days = plan.get("duration_days", 0)
    total_budget = plan.get("total_budget", 0)

    spent_so_far = sum(day["spent"] for day in progress)
    days_done = len(progress)

    percent_time = (days_done / total_days) * 100 if total_days else 0
    percent_budget = (spent_so_far / total_budget) * 100 if total_budget else 0

    return (
        f"📊 Tiến độ: {days_done}/{total_days} ngày ({percent_time:.1f}%)\n"
        f"💰 Ngân sách đã dùng: {spent_so_far}/{total_budget} ({percent_budget:.1f}%)\n"
        f"{'⚠️ Bạn đang tiêu vượt dự kiến!' if percent_budget > percent_time else '✅ Bạn đang theo đúng ngân sách.'}"
    )
