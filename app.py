import streamlit as st
import requests

st.set_page_config(page_title="SALEH AI GOLD", page_icon="👑")

# المفاتيح
api_keys = [
    "AIzaSyA83bkpXNvLB7bmcqOpDi7ucGYqI7K7kD4",
    "AIzaSyCRGxh0HeSmv0QV3BP65yMuWiltDxEskl4"
]

if "key_index" not in st.session_state:
    st.session_state.key_index = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("👑 SALEH AI - ULTIMATE")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تحدث مع صالح AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        success = False
        # هنجرب أكتر من موديل بالترتيب لغاية ما واحد يوافق يشتغل
        models_to_try = ["gemini-1.5-pro", "gemini-1.0-pro", "gemini-pro"]
        
        for model_name in models_to_try:
            if success: break
            
            for _ in range(len(api_keys)):
                current_key = api_keys[st.session_state.key_index]
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={current_key}"
                headers = {'Content-Type': 'application/json'}
                payload = {"contents": [{"parts": [{"text": prompt}]}]}

                try:
                    response = requests.post(url, headers=headers, json=payload)
                    result = response.json()

                    if response.status_code == 200:
                        text_response = result['candidates'][0]['content']['parts'][0]['text']
                        st.markdown(text_response)
                        st.session_state.messages.append({"role": "assistant", "content": text_response})
                        success = True
                        break
                    elif response.status_code == 429:
                        st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
                        continue
                except:
                    continue
        
        if not success:
            st.error("صالح، جوجل حالياً مانعة الوصول للموديلات المجانية في منطقتك. حاول تغيير الـ API Key من إيميل جديد تماماً أو انتظر قليلاً.")
