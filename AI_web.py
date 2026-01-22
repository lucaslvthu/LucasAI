import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# 1. Cấu hình
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    client = MongoClient(st.secrets["MONGO_URL"])
    db = client["LucasAI_DB"]
    history_col = db["chat_history"]
except Exception as e:
    st.error(f"Lỗi cấu hình: {e}")

# 2. TỰ ĐỘNG TÌM MODEL CHẠY ĐƯỢC (Sửa triệt để lỗi 404)
@st.cache_resource
def get_working_model():
    # Thử danh sách các tên model phổ biến nhất
    for model_name in ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro']:
        try:
            m = genai.GenerativeModel(model_name)
            # Thử tạo một nội dung ngắn để kiểm tra xem model có tồn tại không
            m.generate_content("hi") 
            return m
        except:
            continue
    return None

model = get_working_model()

st.title("🤖 Trợ lý Lucas AI")

if model:
    st.success(f"Hệ thống đã sẵn sàng!")
else:
    st.error("Lỗi: Không tìm thấy model nào phù hợp với API Key này. Hãy thử tạo lại API Key mới trên Google AI Studio.")

# 3. Giao diện chat
user_input = st.text_input("Nhập câu hỏi:")

if user_input and model:
    try:
        response = model.generate_content(user_input)
        if response.text:
            st.markdown(f"**AI trả lời:** {response.text}")
            # Lưu vào MongoDB
            history_col.insert_one({"q": user_input, "a": response.text})
            st.toast("Đã lưu trí nhớ!")
    except Exception as e:
        st.error(f"Lỗi khi trả lời: {e}")
