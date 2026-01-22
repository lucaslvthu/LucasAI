import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient
import os

# 1. Cấu hình bảo mật
try:
    # Ép buộc sử dụng phiên bản v1 thay vì v1beta để tránh lỗi 404
    os.environ["GOOGLE_API_USE_G2_MODEL_NAMES"] = "true"
    
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    client = MongoClient(st.secrets["MONGO_URL"])
    db = client["LucasAI_DB"]
    history_col = db["chat_history"]
except Exception as e:
    st.error(f"Lỗi cấu hình: {e}")

# 2. KHỞI TẠO MODEL (Dùng tên chính xác nhất cho phiên bản v1)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 Trợ lý Lucas AI")
st.success("Hệ thống đã sẵn sàng chiến đấu!")

user_input = st.text_input("Nhập câu hỏi của bạn:", placeholder="Ví dụ: Chào bạn...")

if user_input:
    try:
        # Gọi AI trả lời
        response = model.generate_content(user_input)
        
        if response and response.text:
            st.markdown(f"**AI trả lời:** \n\n {response.text}")
            
            # Lưu vào MongoDB
            history_col.insert_one({"question": user_input, "answer": response.text})
            st.toast("✅ Đã ghi nhớ!")
    except Exception as e:
        # Hiển thị lỗi chi tiết để xử lý nếu vẫn còn
        st.error(f"Lỗi: {e}")
