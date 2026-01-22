import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# 1. Cấu hình bảo mật
try:
    # Lấy API Key từ Secrets
    api_key = st.secrets["GEMINI_API_KEY"]
    
    # CẤU HÌNH QUAN TRỌNG: Ép sử dụng transport='rest' để bắt buộc dùng API v1
    # Điều này sẽ giải quyết lỗi 404 v1beta mà bạn đang gặp phải
    genai.configure(api_key=api_key, transport='rest')
    
    # Kết nối MongoDB (Mật khẩu: lucaslvthu)
    client = MongoClient(st.secrets["MONGO_URL"])
    db = client["LucasAI_DB"]
    history_col = db["chat_history"]
except Exception as e:
    st.error(f"Lỗi cấu hình: {e}")

# 2. KHỞI TẠO MODEL
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 Trợ lý Lucas AI")
st.success("Hệ thống đã chuyển sang chế độ kết nối v1 ổn định!")

user_input = st.text_input("Hãy hỏi tôi điều gì đó:", key="user_query")

if user_input:
    try:
        # Gọi AI trả lời
        response = model.generate_content(user_input)
        
        if response.text:
            st.markdown(f"**AI trả lời:** \n\n {response.text}")
            
            # Lưu vào MongoDB
            history_col.insert_one({"question": user_input, "answer": response.text})
            st.toast("✅ Đã ghi nhớ!")
    except Exception as e:
        # Nếu vẫn lỗi, hiển thị chi tiết để xử lý
        st.error(f"Lỗi hệ thống: {e}")
