import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# 1. Kết nối hệ thống
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    client = MongoClient(st.secrets["MONGO_URL"])
    db = client["LucasAI_DB"]
    history_col = db["chat_history"]
except Exception as e:
    st.error(f"Lỗi cấu hình: {e}")

# 2. HÀM TỰ ĐỘNG TÌM MODEL (Khắc phục triệt để lỗi 404)
@st.cache_resource
def find_working_model():
    # Thử danh sách model từ mới nhất đến cũ hơn
    available_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    for name in available_names:
        try:
            m = genai.GenerativeModel(name)
            # Thử tạo một phản hồi siêu ngắn để kiểm tra
            m.generate_content("test")
            return m
        except:
            continue
    return None

model = find_working_model()

st.title("🤖 Trợ lý Lucas AI")

if model:
    st.success("Hệ thống đã tìm thấy bộ não AI phù hợp và sẵn sàng!")
else:
    st.error("Không tìm thấy model khả dụng. Lucas hãy thử 'Reboot App' nhé!")

# 3. Giao diện Chat
user_input = st.text_input("Nhập câu hỏi của bạn:", key="user_query")

if user_input and model:
    try:
        with st.spinner('Đang suy nghĩ...'):
            response = model.generate_content(user_input)
            
        if response.text:
            st.markdown(f"**AI trả lời:** \n\n {response.text}")
            
            # Lưu vào MongoDB
            history_col.insert_one({"q": user_input, "a": response.text})
            st.toast("✅ Đã ghi nhớ!")
    except Exception as e:
        st.error(f"Lỗi: {e}")
