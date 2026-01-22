import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# 1. Cấu hình bảo mật từ Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    client = MongoClient(st.secrets["MONGO_URL"])
    db = client["LucasAI_DB"]
    history_col = db["chat_history"]
except Exception as e:
    st.error(f"Lỗi cấu hình: {e}")

# 2. KHỞI TẠO MODEL (Sửa lỗi 404 bằng cách thêm tiền tố models/)
# Đây là chìa khóa để xử lý lỗi NotFound trong logs
model = genai.GenerativeModel('models/gemini-1.5-flash')

st.title("🤖 Trợ lý Lucas AI")
st.success("Hệ thống đã nhận diện API Key mới!")

user_input = st.text_input("Hãy hỏi tôi bất cứ điều gì:", placeholder="Chào Lucas...")

if user_input:
    try:
        # Gọi AI trả lời với tên model đã được chuẩn hóa
        response = model.generate_content(user_input)
        
        if response.text:
            st.markdown(f"**AI trả lời:** \n\n {response.text}")
            
            # Lưu vào MongoDB
            history_col.insert_one({"question": user_input, "answer": response.text})
            st.toast("✅ Đã ghi nhớ vào bộ não MongoDB!")
    except Exception as e:
        # Nếu vẫn lỗi, hiển thị thông tin cụ thể để xử lý
        st.error(f"Lỗi: {e}")
        st.info("Mẹo: Đảm bảo API Key trong Secrets không có khoảng trắng dư thừa.")
