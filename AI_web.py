import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

# 1. Cài đặt API (Lấy từ Secrets của Streamlit)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. Kết nối MongoDB (Lấy từ Secrets của Streamlit)
client = MongoClient(st.secrets["MONGO_URL"])
db = client["LucasAI_DB"]
history_col = db["chat_history"]

# 3. Định nghĩa AI với Instruction
CHỈ_DẪN_HỆ_THỐNG = """
Bạn là một trợ lý đa năng tên là 'Gemini Học Đường'. Bạn có 3 kỹ năng chính:
1. GIẢI TOÁN: Giải chi tiết và hài hước.
2. TÓM TẮT: Tóm tắt văn bản thành 3 dòng gạch đầu dòng.
3. TƯ VẤN VUI: Trả lời như một người bạn thân thiết.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=CHỈ_DẪN_HỆ_THỐNG
)

# 4. Giao diện Web
st.title("🚀 Gemini 1.5 Flash Đa Năng")
st.caption("Trợ lý của Lucas - Có trí nhớ MongoDB")

user_input = st.text_input("Bạn cần giúp gì (Giải toán, Tóm tắt hay Tâm sự)?")

if user_input:
    # Gọi AI trả lời
    response = model.generate_content(user_input)
    st.markdown(f"**Gemini trả lời:** \n\n {response.text}")
    
    # LƯU VÀO MONGODB (Trí nhớ)
    data_to_save = {
        "user_query": user_input,
        "ai_response": response.text
    }
    history_col.insert_one(data_to_save)
    st.success("✅ Đã lưu cuộc trò chuyện vào MongoDB!")
