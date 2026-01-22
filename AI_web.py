import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# 1. Cấu hình bảo mật
try:
    # ÉP BUỘC SỬ DỤNG PHIÊN BẢN v1 (Đây là chìa khóa sửa lỗi 404)
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
    
    client = MongoClient(st.secrets["MONGO_URL"])
    db = client["LucasAI_DB"]
    history_col = db["chat_history"]
except Exception as e:
    st.error(f"Lỗi cấu hình: {e}")

# 2. KHỞI TẠO MODEL (Dùng tên trực tiếp)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 Trợ lý Lucas AI")
st.success("Hệ thống đã nhận diện API và ép xung bản v1!")

user_input = st.text_input("Nhập câu hỏi của bạn:", placeholder="Chào bạn...")

if user_input:
    try:
        # Gọi AI trả lời
        response = model.generate_content(user_input)
        
        if response.text:
            st.markdown(f"**AI trả lời:** \n\n {response.text}")
            
            # Lưu vào MongoDB
            history_col.insert_one({"q": user_input, "a": response.text})
            st.toast("✅ Đã ghi nhớ!")
    except Exception as e:
        # Nếu vẫn lỗi, liệt kê lỗi chi tiết để xử lý
        st.error(f"Lỗi hệ thống: {e}")
