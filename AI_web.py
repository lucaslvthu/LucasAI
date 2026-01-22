import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# 1. Kết nối "Trí nhớ" MongoDB
try:
    client = MongoClient(st.secrets["MONGO_URL"])
    db = client["LucasAI_DB"]
    history_col = db["chat_history"]
except Exception as e:
    st.error("Lỗi kết nối Database!")

# 2. Kết nối "Bộ não" Gemini
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # SỬA LỖI 404: Dùng tên mô hình đầy đủ nhất
    model = genai.GenerativeModel('gemini-1.5-flash-latest') 
except Exception as e:
    st.error("Lỗi kết nối API Key!")

st.title("🤖 Trợ lý Lucas AI")
st.info("Phiên bản ổn định - Đã sửa lỗi 404")

user_input = st.text_input("Hãy hỏi tôi bất cứ điều gì:")

if user_input:
    try:
        # Gọi AI trả lời
        response = model.generate_content(user_input)
        
        if response.text:
            st.markdown(f"**AI trả lời:** \n\n {response.text}")
            
            # Lưu vào MongoDB
            history_col.insert_one({
                "question": user_input, 
                "answer": response.text
            })
            st.success("✅ Đã ghi nhớ cuộc hội thoại!")
    except Exception as e:
        st.error(f"Lỗi: {e}. Thử lại sau 1 phút.")
