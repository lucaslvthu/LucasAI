import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# 1. Cấu hình bảo mật từ Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    client = MongoClient(st.secrets["MONGO_URL"])
    db = client["LucasAI_DB"]
    history_col = db["chat_history"]
except:
    st.error("Lỗi cấu hình Secrets!")

# 2. Khởi tạo Model (Dùng tên mã cơ bản nhất để tránh lỗi 404)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 Trợ lý Lucas AI")
st.info("Phiên bản đã tối ưu hóa thư viện")

user_input = st.text_input("Hãy hỏi tôi bất cứ điều gì:", key="user_query")

if user_input:
    try:
        # Gọi AI trả lời
        response = model.generate_content(user_input)
        
        if response.text:
            st.markdown(f"**AI trả lời:** \n\n {response.text}")
            
            # Lưu vào MongoDB để làm trí nhớ
            history_col.insert_one({
                "question": user_input, 
                "answer": response.text
            })
            st.success("✅ Đã ghi nhớ vào MongoDB!")
    except Exception as e:
        # Nếu vẫn lỗi 404, thử dùng model 1.0 pro
        st.warning("Đang thử kết nối dự phòng...")
        backup_model = genai.GenerativeModel('gemini-pro')
        response = backup_model.generate_content(user_input)
        st.markdown(f"**AI (Dự phòng) trả lời:** \n\n {response.text}")
