import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="SALEH AI", page_icon="👑")

# ستايل ذهبي وفخم
st.markdown("""
    <style>
    .main { background-color: #000000; }
    .stTextInput > div > div > input { color: #D4AF37 !important; background-color: #111 !important; border: 1px solid #D4AF37 !important; }
    .stButton > button { background-color: #D4AF37; color: black; border-radius: 20px; width: 100%; }
    /* ستايل الرسايل */
    [data-testid="stChatMessage"] { background-color: #0a0a0a; border: 1px solid #222; border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("👑 SALEH AI - PRO")

# إعداد API
API_KEY = "AIzaSyD3VJe5eS8WyZpdo98wu9MywGgbks3K2us"
genai.configure(api_key=API_KEY)

# تغيير اسم الموديل ليكون أكثر دقة
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# ذاكرة الشات
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة الإدخال
if prompt := st.chat_input("اسأل صالح AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # استخدام generate_content مباشرة
            response = model.generate_content(prompt)
            full_response = response.text
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            # لو فشل، بيجرب الموديل الأساسي كخيار أخير
            st.error(f"حدث خطأ: {e}")
