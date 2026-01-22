import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# 1. Cấu hình hệ thống (Sử dụng Secrets)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    client = MongoClient(st.secrets["MONGO_URL"])
    db = client["LucasAI_DB"]
    history_col = db["chat_history"]
except Exception as e:
    st.error(f"Lỗi kết nối: {e}")

# 2. KHỞI TẠO MODEL (Chỉ dùng gemini-1.5-flash)
# Tuyệt đối KHÔNG dùng gemini-pro vì sẽ bị lỗi 404 như trong Logs
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 Trợ lý Lucas AI")
st.success("Hệ thống đã sẵn sàng với API mới!")

user_input = st.text_input("Nhập câu hỏi của bạn:", key="user_query")

if user_input:
    try:
        # Gọi AI trả lời
        response = model.generate_content(user_input)
        
        if response.text:
            st.markdown(f"**AI trả lời:** \n\n {response.text}")
            
            # Lưu vào MongoDB để tạo trí nhớ
            history_col.insert_one({
                "question": user_input, 
                "answer": response.text
            })
            st.toast("✅ Đã ghi nhớ!")
    except Exception as e:
        st.error(f"Lỗi: {e}")
