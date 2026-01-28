import streamlit as st
import requests

st.set_page_config(page_title="SALEH AI PRO", page_icon="👑")

# تنسيق الواجهة
st.markdown("""
    <style>
    .main { background-color: #050505; }
    div[data-testid="stChatMessage"] { border-radius: 15px; border: 1px solid #D4AF37; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("👑 SALEH AI - ULTIMATE")

# المفتاح الجديد
NEW_API_KEY = "AIzaSyAap0wkUBLjvHgmKe4sfil8FWgoc3Tfp5M"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تحدث مع صالح AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # هنا التغيير الجذري: نستخدم gemini-pro (النسخة المستقرة 1.0)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={NEW_API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            response = requests.post(url, json=payload, timeout=15)
            result = response.json()
            
            if response.status_code == 200:
                text_response = result['candidates'][0]['content']['parts'][0]['text']
                st.markdown(text_response)
                st.session_state.messages.append({"role": "assistant", "content": text_response})
            else:
                error_msg = result.get('error', {}).get('message', 'خطأ غير معروف')
                # لو لسه فيه مشكلة، هنعرض لك الموديلات اللي جوجل سامحة ليك بيها فعلياً
                st.error(f"جوجل بتقول: {error_msg}")
                st.info("نصيحة: جرب تكتب 'hello' بالإنجليزية، أحياناً الموديلات الجديدة بتطلب لغة إنجليزية في أول رسالة لتفعيل الحساب.")
        except Exception as e:
            st.error(f"فشل الاتصال: {e}")
