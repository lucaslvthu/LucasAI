import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# 1. Kết nối hệ thống
try:
    # Cấu hình API Key
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Kết nối MongoDB
    client = MongoClient(st.secrets["MONGO_URL"])
    db = client["LucasAI_DB"]
    history_col = db["chat_history"]
except Exception as e:
    st.error(f"Lỗi kết nối: {e}")

# 2. KHỞI TẠO MODEL (Dùng tên 'gemini-1.5-flash' - KHÔNG CÓ 'models/')
# Streamlit sẽ tự động tìm phiên bản ổn định nhất
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 Trợ lý Lucas AI")
st.success("Hệ thống đã sẵn sàng!")

user_input = st.text_input("Nhập câu hỏi của bạn:", key="user_query")

if user_input:
    try:
        # Gọi AI trả lời
        # Chúng ta dùng phương thức cơ bản nhất để tránh lỗi version
        response = model.generate_content(user_input)
        
        if response.text:
            st.markdown(f"**AI trả lời:** \n\n {response.text}")
            
            # Lưu vào MongoDB
            history_col.insert_one({"q": user_input, "a": response.text})
            st.toast("✅ Đã ghi nhớ!")
            
    except Exception as e:
        # Nếu vẫn lỗi 404, thử phương án cuối cùng: Gọi tên đầy đủ
        try:
            model_alt = genai.GenerativeModel('models/gemini-1.5-flash')
            response_alt = model_alt.generate_content(user_input)
            st.markdown(f"**AI trả lời:** \n\n {response_alt.text}")
        except:
            st.error(f"Lỗi: {e}")
            st.info("Lucas hãy kiểm tra lại xem trong mục Secrets đã nhấn nút SAVE chưa nhé!")
