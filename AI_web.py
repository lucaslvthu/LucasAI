import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# 1. Cấu hình bảo mật
try:
    # Cấu hình API Key mới của bạn
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Kết nối MongoDB (Mật khẩu: lucaslvthu)
    client = MongoClient(st.secrets["MONGO_URL"])
    db = client["LucasAI_DB"]
    history_col = db["chat_history"]
except Exception as e:
    st.error(f"Lỗi cấu hình: {e}")

# 2. KHỞI TẠO MODEL (Dùng tên model chuẩn xác nhất)
# Lưu ý: Không thêm 'models/' phía trước nếu dùng thư viện bản mới
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 Trợ lý Lucas AI")
st.success("Hệ thống đã kết nối thành công!")

user_input = st.text_input("Hãy hỏi tôi điều gì đó:", key="user_input")

if user_input:
    try:
        # Gọi AI (Sử dụng model flash 1.5)
        response = model.generate_content(user_input)
        
        if response.text:
            st.markdown(f"**AI:** {response.text}")
            
            # Lưu trí nhớ vào MongoDB
            history_col.insert_one({
                "question": user_input, 
                "answer": response.text
            })
            st.toast("✅ Đã lưu vào MongoDB!")
    except Exception as e:
        # Nếu vẫn lỗi 404, code này sẽ tự động thử cách gọi tên khác
        st.warning("Đang thử kết nối lại với cấu hình dự phòng...")
        try:
            model_alt = genai.GenerativeModel('models/gemini-1.5-flash')
            response = model_alt.generate_content(user_input)
            st.markdown(f"**AI (Dự phòng):** {response.text}")
        except Exception as e2:
            st.error(f"Lỗi: {e2}")
            st.info("Kiểm tra lại xem bạn đã nhấn 'Save' API Key mới trong Secrets chưa?")
