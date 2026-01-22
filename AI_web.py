import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# 1. Cấu hình bảo mật từ Secrets
try:
    # Sử dụng API Key mới mà bạn vừa tạo
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Kết nối MongoDB (Mật khẩu: lucaslvthu)
    client = MongoClient(st.secrets["MONGO_URL"])
    db = client["LucasAI_DB"]
    history_col = db["chat_history"]
except Exception as e:
    st.error(f"Lỗi cấu hình: {e}")

# 2. KHỞI TẠO MODEL (Dùng đúng bản 1.5 Flash - bản Google AI Studio đang chạy)
# Không dùng tiền tố models/ để tránh xung đột phiên bản v1beta
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 Trợ lý Lucas AI")
st.success("Hệ thống đã sẵn sàng với API Key mới!")

# Ô nhập liệu
user_input = st.text_input("Nhập câu hỏi của bạn:", placeholder="Hỏi AI bất cứ điều gì...")

if user_input:
    try:
        # Gọi AI trả lời
        with st.spinner('AI đang trả lời...'):
            response = model.generate_content(user_input)
        
        if response.text:
            st.markdown(f"**AI trả lời:** \n\n {response.text}")
            
            # LƯU VÀO MONGODB
            history_col.insert_one({
                "question": user_input, 
                "answer": response.text
            })
            st.toast("✅ Đã lưu vào trí nhớ!")
    except Exception as e:
        st.error(f"Lỗi: {e}")
        st.info("Mẹo: Nếu vẫn thấy lỗi 404, hãy kiểm tra lại Secrets đã Save API Key mới chưa.")
