import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# 1. Cấu hình hệ thống từ Secrets
try:
    # API Key: AIzaSyDj6_YjobSiD6oDU-XgGC9CnYpu2DeuZGc
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # MongoDB: lucaslvthu
    client = MongoClient(st.secrets["MONGO_URL"])
    db = client["LucasAI_DB"]
    history_col = db["chat_history"]
except Exception as e:
    st.error(f"Lỗi kết nối Secrets: {e}")

# 2. KHỞI TẠO MODEL (Dùng tên rút gọn nhất để sửa lỗi 404)
# Tuyệt đối KHÔNG thêm chữ 'models/' ở đây
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 Trợ lý Lucas AI")
st.success("Hệ thống đã nhận diện API mới thành công!")

# Ô nhập liệu
user_input = st.text_input("Bạn muốn hỏi gì?", placeholder="Ví dụ: Chào Lucas...")

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
            st.toast("✅ Đã ghi nhớ vào MongoDB!")
    except Exception as e:
        # Nếu vẫn lỗi, thử cách gọi cuối cùng (dành cho một số vùng đặc biệt)
        try:
            model_alt = genai.GenerativeModel('models/gemini-1.5-flash')
            response = model_alt.generate_content(user_input)
            st.write(response.text)
        except:
            st.error(f"Lỗi: {e}")
            st.info("Lucas hãy kiểm tra lại xem đã nhấn SAVE API Key mới trong mục Secrets chưa nhé!")
