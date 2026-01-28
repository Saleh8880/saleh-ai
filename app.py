import streamlit as st
import requests

# --- 1. الإعدادات والتصميم (الشكل اللي طلبته) ---
st.set_page_config(page_title="SALEH AI PRO", page_icon="👑")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; }
    .stApp { background-color: #0e1117; }
    h1 { color: #FFD700 !important; text-align: center; border-bottom: 1px solid #333; padding-bottom: 20px; }
    .stChatMessage { background-color: #262730; border-radius: 10px; margin-bottom: 10px; }
    .stTextInput > div > div > input { background-color: #1E1E1E; color: white; border-radius: 20px; }
</style>
""", unsafe_allow_html=True)

NEW_API_KEY = "AIzaSyAap0wkUBLjvHgmKe4sfil8FWgoc3Tfp5M"

st.title("👑 SALEH AI - ULTIMATE")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. عرض المحادثة ---
for message in st.session_state.messages:
    avatar = "👑" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- 3. دالة اختيار الموديل (مع التعديل البسيط لتفادي الخطأ) ---
def find_any_working_model():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={NEW_API_KEY}"
    try:
        response = requests.get(url)
        models_data = response.json()
        
        for m in models_data.get('models', []):
            # --- السطر ده هو اللي بيحل المشكلة ---
            # بنقوله لو اسم الموديل فيه "2.5" فكك منه وشوف اللي بعده
            if '2.5' in m['name']:
                continue 
            # ------------------------------------
            
            if 'generateContent' in m.get('supportedGenerationMethods', []):
                return m['name']
        
        return "models/gemini-pro"
    except:
        return "models/gemini-pro"

# --- 4. التشغيل ---
if prompt := st.chat_input("اسأل صالح AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.markdown(prompt)

    with st.chat_message("assistant", avatar="👑"):
        try:
            working_model = find_any_working_model()
            
            url = f"https://generativelanguage.googleapis.com/v1beta/{working_model}:generateContent?key={NEW_API_KEY}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            
            res = requests.post(url, json=payload)
            data = res.json()
            
            if res.status_code == 200:
                ans = data['candidates'][0]['content']['parts'][0]['text']
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            else:
                st.error(f"خطأ: الموديل {working_model} رفض الرد (Code: {res.status_code})")
        
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
