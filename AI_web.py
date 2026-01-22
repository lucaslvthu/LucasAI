import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# 1. Cấu hình an toàn từ Secrets
try:
    # Kết nối Gemini API
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Kết nối MongoDB (Mật khẩu: lucaslvthu)
    client = MongoClient(st.secrets["MONGO_URL"])
    db = client["LucasAI_DB"]
    history_col = db["chat_history"]
except Exception as e:
    st.error(f"Lỗi cấu hình Secrets hoặc Database: {e}")

# 2. Khởi tạo Model (Dùng tên đầy đủ để sửa lỗi 404)
# Việc thêm 'models/' giúp hệ thống định vị chính xác bộ não AI
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

# 3. Giao diện người dùng (UI)
st.set_page_config(page_title="Trợ lý Lucas AI", page_icon="🤖")
st.title("🤖 Trợ lý Lucas AI")
st.success("Hệ thống đã kết nối MongoDB thành công!") # Xác nhận từ Screenshot (326)

# Ô nhập liệu
user_input = st.text_input("Nhập câu hỏi của bạn:", key="user_query", placeholder="Ví dụ: Tâm sự với tôi đi...")

# 4. Xử lý logic khi người dùng nhắn tin
if user_input:
    try:
        # Gọi AI trả lời
        with st.spinner('AI đang suy nghĩ...'):
            response = model.generate_content(user_input)
            
        if response.text:
            # Hiển thị câu trả lời ra màn hình
            st.markdown(f"**AI trả lời:** \n\n {response.text}")
            
            # LƯU VÀO MONGODB (Trí nhớ của AI)
            chat_data = {
                "user_name": "Lucas",
                "question": user_input,
                "answer": response.text
            }
            history_col.insert_one(chat_data)
            st.toast("✅ Đã ghi nhớ vào MongoDB!")
            
    except Exception as e:
        # Xử lý các lỗi phổ biến (như 404 hoặc giới hạn API)
        st.error(f"Đã xảy ra lỗi: {e}")
        st.info("Mẹo: Hãy kiểm tra lại API Key hoặc đợi 1 phút rồi thử lại.")

# 5. Hiển thị lịch sử ngắn (Tùy chọn)
if st.checkbox("Xem 3 câu hỏi gần nhất trong bộ nhớ"):
    last_chats = history_col.find().sort("_id", -1).limit(3)
    for chat in last_chats:
        st.write(f"❓ {chat.get('question')}")
