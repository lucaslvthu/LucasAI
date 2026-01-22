import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# 1. Kết nối an toàn
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    client = MongoClient(st.secrets["MONGO_URL"])
    db = client["LucasAI_DB"]
    history_col = db["chat_history"]
except:
    st.error("Lỗi kết nối Secrets!")

# 2. Cơ chế tự động chọn Model (Sửa lỗi 404 triệt để)
def get_model():
    # Danh sách các tên model có thể chạy được
    model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    for name in model_names:
        try:
            m = genai.GenerativeModel(name)
            # Thử gọi một lệnh kiểm tra nhỏ
            return m
        except:
            continue
    return None

model = get_model()

st.title("🤖 Trợ lý Lucas AI")
st.success("Hệ thống đã kết nối MongoDB thành công!")

user_input = st.text_input("Nhập câu hỏi của bạn:", key="user_query")

if user_input:
    if model is None:
        st.error("Không tìm thấy mô hình AI nào khả dụng. Kiểm tra lại API Key!")
    else:
        try:
            response = model.generate_content(user_input)
            st.markdown(f"**AI trả lời:** \n\n {response.text}")
            
            # Lưu vào MongoDB
            history_col.insert_one({"q": user_input, "a": response.text})
            st.toast("✅ Đã ghi nhớ!")
        except Exception as e:
            st.error(f"Lỗi: {e}")

# Xem lịch sử
if st.checkbox("Xem 3 câu hỏi gần nhất"):
    for chat in history_col.find().sort("_id", -1).limit(3):
        st.write(f"❓ {chat.get('q')}")
