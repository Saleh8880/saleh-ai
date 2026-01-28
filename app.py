import streamlit as st
import requests

st.set_page_config(page_title="SALEH AI PRO", page_icon="👑")

st.markdown("""
    <style>
    .main { background-color: #050505; }
    div[data-testid="stChatMessage"] { border-radius: 15px; border: 1px solid #D4AF37; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("👑 SALEH AI - ULTIMATE")

# المفتاح الجديد بتاعك
NEW_API_KEY = "AIzaSyAap0wkUBLjvHgmKe4sfil8FWgoc3Tfp5M"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسأل صالح AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # التعديل الجوهري: استخدام v1 بدلاً من v1beta واسم الموديل الكامل
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={NEW_API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            response = requests.post(url, json=payload, timeout=15)
            result = response.json()
            
            if response.status_code == 200:
                text_response = result['candidates'][0]['content']['parts'][0]['text']
                st.markdown(text_response)
                st.session_state.messages.append({"role": "assistant", "content": text_response})
            else:
                # لو لسه فيه مشكلة، هنخلي الكود يطبع لنا الرد بالكامل عشان نفهمه
                st.error(f"رد جوجل: {result}")
        except Exception as e:
            st.error(f"فشل الاتصال: {e}")
