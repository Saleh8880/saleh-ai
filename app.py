import streamlit as st
import requests

# إعدادات واجهة صالح الفخمة
st.set_page_config(page_title="SALEH AI PRO", page_icon="👑")

st.markdown("""
    <style>
    .main { background-color: #050505; }
    div[data-testid="stChatMessage"] { border-radius: 15px; border: 1px solid #D4AF37; color: white; }
    .stChatInputContainer { padding-bottom: 20px; }
    h1 { color: #D4AF37; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("👑 SALEH AI - ULTIMATE")

# المفتاح الجديد اللي أنت بعته
NEW_API_KEY = "AIzaSyAap0wkUBLjvHgmKe4sfil8FWgoc3Tfp5M"

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسأل صالح AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        success = False
        # هنجرب أكتر من موديل بالمفتاح الجديد عشان نضمن الرد
        models = ["gemini-1.5-flash", "gemini-1.5-pro"]
        
        for model_name in models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={NEW_API_KEY}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            
            try:
                response = requests.post(url, json=payload, timeout=10)
                result = response.json()
                
                if response.status_code == 200:
                    text_response = result['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(text_response)
                    st.session_state.messages.append({"role": "assistant", "content": text_response})
                    success = True
                    break
                else:
                    # لو الموديل ده مش متاح، جرب اللي بعده
                    continue
            except:
                continue
        
        if not success:
            st.error("صالح، جوجل لسه مش قادرة تتعرف على الموديل. جرب تعمل Refresh للمتصفح.")
