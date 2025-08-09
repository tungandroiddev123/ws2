import streamlit as st
from utils import (
    generate_plan,
    save_user_conversation,
    get_user_conversation,
    update_trip_progress,
    compare_with_plan,
    list_conversations,
    create_new_conversation,
    chat_with_ai
)

st.set_page_config(page_title="AI Travel Planner", page_icon="🌍")

# Giả sử user_id cố định (thực tế có thể dùng login)
USER_ID = "user123"

# Khởi tạo session_state
if "current_conv_id" not in st.session_state:
    if not list_conversations(USER_ID):
        st.session_state.current_conv_id = create_new_conversation(USER_ID)
    else:
        st.session_state.current_conv_id = list_conversations(USER_ID)[0]

# Chọn hội thoại
st.sidebar.title("💬 Conversations")
conv_list = list_conversations(USER_ID)
selected_conv = st.sidebar.selectbox(
    "Select conversation",
    conv_list,
    index=conv_list.index(st.session_state.current_conv_id)
)
st.session_state.current_conv_id = selected_conv

# Nút tạo mới
if st.sidebar.button("➕ New Conversation"):
    new_id = create_new_conversation(USER_ID)
    st.session_state.current_conv_id = new_id
    st.rerun()

# Load conversation hiện tại
conversation_data = get_user_conversation(USER_ID, st.session_state.current_conv_id)
conversation = conversation_data["messages"]  # ✅ chỉ lấy messages

# Hiển thị hội thoại
for msg in conversation:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").markdown(msg["content"])

# Nhập input chat
if prompt := st.chat_input("Type your message..."):
    conversation.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    with st.spinner("Thinking..."):
        reply = chat_with_ai(conversation)

    conversation.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").markdown(reply)

    save_user_conversation(USER_ID, st.session_state.current_conv_id, conversation)

# Nút reset hội thoại hiện tại
if st.sidebar.button("♻️ Reset Current Conversation"):
    from prompts import AI_TRAVEL_PLANNER_PROMPT
    conversation = [{"role": "system", "content": AI_TRAVEL_PLANNER_PROMPT}]
    save_user_conversation(USER_ID, st.session_state.current_conv_id, conversation)
    st.rerun()

tab1, tab2 = st.tabs(["💬 Chatbot", "📍 Tracking"])

with tab2:
    st.subheader("Theo dõi chuyến đi")
    day = st.number_input("Ngày", min_value=1, step=1)
    completed = st.text_area("Hoạt động đã hoàn thành (cách nhau bằng dấu ,)")
    spent = st.number_input("Chi tiêu hôm nay", min_value=0.0, step=1.0)

    if st.button("Cập nhật tiến độ"):
        update_trip_progress(
            USER_ID,
            st.session_state.current_conv_id,
            day,
            completed.split(",") if completed else [],
            spent
        )
        st.success("Đã cập nhật tiến độ!")

    if st.button("So sánh với kế hoạch"):
        st.info(compare_with_plan(USER_ID, st.session_state.current_conv_id))
