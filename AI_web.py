import streamlit as st
import google.generativeai as genai

# 1. Cài đặt API (Lấy key tại Google AI Studio)
genai.configure(api_key="YOUR_API_KEY")

# 2. Định nghĩa "Đa nhiệm" bằng System Instruction
# Đây là nơi bạn dạy AI các kỹ năng khác nhau
CHỈ_DẪN_HỆ_THỐNG = """
Bạn là một trợ lý đa năng tên là 'Gemini Học Đường'. Bạn có 3 kỹ năng chính:
1. GIẢI TOÁN: Nếu người dùng hỏi về toán, hãy giải chi tiết và hài hước.
2. TÓM TẮT: Nếu người dùng đưa vào một đoạn văn dài, hãy tóm tắt nó thành 3 dòng gạch đầu dòng.
3. TƯ VẤN VUI: Nếu người dùng hỏi về cuộc sống, hãy trả lời như một người bạn thân thiết.
Nếu câu hỏi không thuộc 3 nhóm trên, hãy trả lời ngắn gọn và lịch sự.
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=CHỈ_DẪN_HỆ_THỐNG
)

# 3. Giao diện Web đơn giản bằng Streamlit
st.title("🚀 Gemini 2.5 Flash Đa Năng")
user_input = st.text_input("Bạn cần giúp gì (Giải toán, Tóm tắt hay Tâm sự)?")

if user_input:
    response = model.generate_content(user_input)
    st.markdown(f"**Gemini trả lời:** \n\n {response.text}")