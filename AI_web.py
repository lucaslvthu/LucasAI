import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# 1. Kết nối "Trí nhớ" MongoDB
try:
    client = MongoClient(st.secrets["MONGO_URL"])
    db = client["LucasAI_DB"]
    history_col = db["chat_history"]
except:
    st.error("Lỗi kết nối cơ sở dữ liệu!")

# 2. Cấu hình AI (Sửa lỗi 404)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Thử dùng tên model chính xác nhất hiện nay
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 Trợ lý Lucas AI")
st.success("Hệ thống đã kết nối MongoDB thành công!")

user_input = st.text_input("Nhập câu hỏi của bạn:", key="user_query")

if user_input:
    try:
        response = model.generate_content(user_input)
        if response.text:
            st.markdown(f"**AI trả lời:** \n\n {response.text}")
            
            # Lưu vào MongoDB
            history_col.insert_one({
                "question": user_input, 
                "answer": response.text
            })
            st.toast("✅ Đã ghi nhớ vào bộ não!")
    except Exception as e:
        st.error(f"Lỗi: {e}")
