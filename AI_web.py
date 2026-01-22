import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# Kết nối an toàn
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
client = MongoClient(st.secrets["MONGO_URL"])
db = client["LucasAI_DB"]
history_col = db["chat_history"]

# Sử dụng model cơ bản nhất để chắc chắn chạy
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 Trợ lý Lucas AI")
st.info("Hệ thống đã được hạ cấp để đảm bảo ổn định")

user_input = st.text_input("Nhập câu hỏi của bạn:")

if user_input:
    try:
        response = model.generate_content(user_input)
        st.write(response.text)
        # Lưu trí nhớ
        history_col.insert_one({"q": user_input, "a": response.text})
        st.success("Đã lưu vào MongoDB!")
    except Exception as e:
        st.error(f"Lỗi: {e}")
