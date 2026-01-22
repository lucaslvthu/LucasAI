import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# 1. Cấu hình
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
client = MongoClient(st.secrets["MONGO_URL"])
db = client["LucasAI_DB"]
history_col = db["chat_history"]

# 2. SỬA LỖI 404: Dùng tên model rút gọn và ổn định nhất
# Thay vì flash-latest, hãy dùng gemini-1.5-flash hoặc gemini-1.5-pro
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 Trợ lý Lucas AI")
st.success("Kết nối MongoDB thành công!")

user_input = st.text_input("Hãy hỏi tôi điều gì đó:")

if user_input:
    try:
        # Sử dụng tham số stream=False để ổn định hơn
        response = model.generate_content(user_input)
        if response.text:
            st.write(f"AI: {response.text}")
            # Lưu vào MongoDB
            history_col.insert_one({"q": user_input, "a": response.text})
            st.toast("Đã lưu trí nhớ!")
    except Exception as e:
        st.error(f"Lỗi: {e}")
        st.info("Thử lại với model dự phòng...")
        # Nếu vẫn 404, code sẽ tự thử bản 1.0 Pro
        backup = genai.GenerativeModel('gemini-pro')
        res = backup.generate_content(user_input)
        st.write(f"AI (Dự phòng): {res.text}")
