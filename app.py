import streamlit as st
import requests

st.set_page_config(page_title="SALEH AI GOLD", page_icon="👑")

# المفاتيح اللي معاك
api_keys = [
    "AIzaSyA83bkpXNvLB7bmcqOpDi7ucGYqI7K7kD4",
    "AIzaSyCRGxh0HeSmv0QV3BP65yMuWiltDxEskl4"
]

if "key_index" not in st.session_state:
    st.session_state.key_index = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("👑 SALEH AI - ULTIMATE")

# عرض الشات
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسأل صالح AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        success = False
        for _ in range(len(api_keys)):
            current_key = api_keys[st.session_state.key_index]
            # نداء مباشر لـ API جوجل الإصدار المستقر v1
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={current_key}"
            headers = {'Content-Type': 'application/json'}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }

            try:
                response = requests.post(url, headers=headers, json=payload)
                result = response.json()

                if response.status_code == 200:
                    text_response = result['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(text_response)
                    st.session_state.messages.append({"role": "assistant", "content": text_response})
                    success = True
                    break
                elif response.status_code == 429: # ضغط رسايل
                    st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
                    continue
                else:
                    st.error(f"خطأ من جوجل: {result.get('error', {}).get('message', 'خطأ غير معروف')}")
                    break
            except Exception as e:
                st.error(f"فشل الاتصال: {e}")
                break
        
        if not success and response.status_code == 429:
            st.warning("⚠️ صالح، المفاتيح مجهدة حالياً. استنى 30 ثانية وجرب تاني.")
