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
    st.error(f"Lỗi cấu hình: {e}")

# 2. CHỐT MODEL: Chỉ dùng duy nhất gemini-1.5-flash
# Đây là model mà API của bạn hỗ trợ tốt nhất
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 Trợ lý Lucas AI")
st.success("Hệ thống đã sẵn sàng!")

user_input = st.text_input("Nhập câu hỏi của bạn:", placeholder="Ví dụ: Chào bạn...")

if user_input:
    try:
        # Gọi AI (Không dùng bản pro cũ để tránh lỗi 404)
        response = model.generate_content(user_input)
        
        if response.text:
            st.markdown(f"**AI trả lời:** \n\n {response.text}")
            
            # Lưu vào MongoDB
            history_col.insert_one({"question": user_input, "answer": response.text})
            st.toast("✅ Đã lưu vào trí nhớ!")
    except Exception as e:
        st.error(f"Lỗi hệ thống: {e}")
