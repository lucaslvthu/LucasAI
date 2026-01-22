import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# 1. Cấu hình bảo mật
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    client = MongoClient(st.secrets["MONGO_URL"])
    db = client["LucasAI_DB"]
    history_col = db["chat_history"]
except Exception as e:
    st.error("Lỗi cấu hình Secrets. Kiểm tra lại bảng Secrets trên Streamlit!")

# 2. Khởi tạo Model (Dùng tên chính xác)
model = genai.GenerativeModel('models/gemini-1.5-flash')

st.title("🚀 Gemini 1.5 Flash Đa Năng")
st.caption("Trợ lý của Lucas - Có trí nhớ MongoDB")

user_input = st.text_input("Bạn cần giúp gì?")

# 3. Xử lý phản hồi (Dòng gây lỗi cũ đã được bọc lại)
if user_input:
    try:
        response = model.generate_content(user_input)
        if response:
            st.markdown(f"**AI trả lời:** \n\n {response.text}")
            # Lưu vào MongoDB
            history_col.insert_one({"question": user_input, "answer": response.text})
            st.success("✅ Đã ghi nhớ vào MongoDB!")
    except Exception as e:
        st.error(f"Đã xảy ra lỗi: {e}")

