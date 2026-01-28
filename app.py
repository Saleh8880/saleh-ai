import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="SALEH AI", page_icon="👑")

# ستايل ذهبي وفخم
st.markdown("""
    <style>
    .main { background-color: #000000; }
    .stTextInput > div > div > input { color: #D4AF37; background-color: #111; border: 1px solid #D4AF37; }
    .stButton > button { background-color: #D4AF37; color: black; border-radius: 20px; width: 100%; }
    .chat-bubble { padding: 10px; border-radius: 15px; margin: 5px; border: 1px solid #D4AF37; }
    </style>
    """, unsafe_allow_config=True)

st.title("👑 SALEH AI - PRO")

# إعداد API
API_KEY = "AIzaSyD3VJe5eS8WyZpdo98wu9MywGgbks3K2us"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ذاكرة الشات
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل القديمة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة الإدخال
if prompt := st.chat_input("اسأل صالح AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        full_response = response.text
        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})