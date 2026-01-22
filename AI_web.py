import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# 1. Cấu hình từ Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    client = MongoClient(st.secrets["MONGO_URL"])
    db = client["LucasAI_DB"]
    history_col = db["chat_history"]
except Exception as e:
    st.error("Chưa cấu hình xong Secrets trên Streamlit!")

# 2. Khởi tạo Model (Sửa lỗi 404 bằng cách dùng tên model chuẩn)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🚀 Gemini 1.5 Flash Đa Năng")
st.caption("Trợ lý của Lucas - Có trí nhớ MongoDB")

user_input = st.text_input("Bạn cần giúp gì?")

if user_input:
    try:
        # Gọi AI trả lời
        response = model.generate_content(user_input)
        if response.text:
            st.markdown(f"**AI trả lời:** \n\n {response.text}")
            # Lưu vào MongoDB
            history_col.insert_one({"question": user_input, "answer": response.text})
            st.success("✅ Đã ghi nhớ vào MongoDB!")
    except Exception as e:
        st.error(f"Đã xảy ra lỗi: {e}")
