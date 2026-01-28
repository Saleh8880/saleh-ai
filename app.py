import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="SALEH AI PRO", page_icon="👑")

# ستايل CSS
st.markdown("""<style>.main { background-color: #050505; } div[data-testid="stChatMessage"] { border-radius: 20px; border: 1px solid #333; }</style>""", unsafe_allow_html=True)

st.title("👑 SALEH AI - PRO")

API_KEY = "AIzaSyA83bkpXNvLB7bmcqOpDi7ucGYqI7K7kD4"
genai.configure(api_key=API_KEY)

# مصفوفة للموديلات عشان لو واحد عليه ضغط نجرب التاني
models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro']

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تحدث مع ذكاء صالح..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("جاري الاتصال بسيرفرات جوجل..."):
            success = False
            for model_name in models_to_try:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    success = True
                    break # لو اشتغل خلاص نخرج من اللوب
                except Exception as e:
                    if "429" in str(e):
                        continue # لو ضغط جرب الموديل اللي بعده
                    else:
                        st.error(f"خطأ: {e}")
                        break
            
            if not success:
                st.warning("⚠️ ضغط كبير على السيرفر المجاني حالياً. يا صالح، انتظر 30 ثانية وجرب تبعت تاني عشان جوجل تسمح لنا بالمرور.")
