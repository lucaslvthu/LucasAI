import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# 1. Cấu hình bảo mật
try:
    # Kết nối Gemini với API Key mới của Lucas
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Kết nối MongoDB với mật khẩu lucaslvthu
    client = MongoClient(st.secrets["MONGO_URL"])
    db = client["LucasAI_DB"]
    history_col = db["chat_history"]
except Exception as e:
    st.error(f"Lỗi cấu hình: {e}")

# 2. KHỞI TẠO MODEL (Dùng tên rút gọn - Cách này thường thành công nhất)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 Trợ lý Lucas AI")
st.success("Hệ thống đã sẵn sàng!")

# Ô nhập liệu
user_input = st.text_input("Nhập câu hỏi của bạn:", placeholder="Chào Lucas...")

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
            st.toast("✅ Đã lưu vào trí nhớ MongoDB!")
    except Exception as e:
        # Nếu vẫn gặp lỗi 404, thử thêm tiền tố 'models/' tự động
        try:
            model_alt = genai.GenerativeModel('models/gemini-1.5-flash')
            response = model_alt.generate_content(user_input)
            st.markdown(f"**AI trả lời:** \n\n {response.text}")
        except:
            st.error(f"Lỗi: {e}. Hãy kiểm tra lại API Key trong Secrets.")
