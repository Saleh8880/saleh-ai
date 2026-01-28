import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="SALEH AI PRO", page_icon="👑", layout="centered")

# 2. تحسين الشكل (التصميم الدوار والخطوط الواضحة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* الخلفية والخط */
    .stApp {
        background-color: #000;
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }

    /* العنوان الرئيسي */
    .main-title {
        color: #D4AF37;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        text-shadow: 0 0 15px rgba(212, 175, 55, 0.6);
        margin-bottom: 5px;
    }

    /* تأثير المربع الذهبي الدوار للرسائل */
    .msg-card {
        position: relative;
        padding: 2px;
        border-radius: 15px;
        overflow: hidden;
        margin-bottom: 20px;
        width: fit-content;
        max-width: 85%;
    }
    
    .msg-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, #D4AF37, transparent, #8A6D3B, transparent);
        animation: rotateMsg 3s linear infinite;
        z-index: 0;
    }

    @keyframes rotateMsg {
        100% { transform: rotate(360deg); }
    }

    .msg-content {
        position: relative;
        z-index: 1;
        background: #0a0a0a;
        border-radius: 13px;
        padding: 15px 20px;
        color: #fff;
        font-size: 17px;
        line-height: 1.6;
    }

    /* تحسين منطقة الإدخال */
    .stChatInputContainer {
        padding-bottom: 30px !important;
    }
    
    .stChatInput div {
        border: 1px solid #D4AF37 !important;
        border-radius: 50px !important;
        background-color: #111 !important;
    }

    /* إخفاء شعارات ستريم ليت */
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">👑 SALEH AI PRO</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>مساعدك الشخصي بأقوى تصميم ذهبي</p>", unsafe_allow_html=True)

# --- المحرك الشغال (لم يتم تغييره لضمان الاستقرار) ---
NEW_API_KEY = "AIzaSyAap0wkUBLjvHgmKe4sfil8FWgoc3Tfp5M"

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل بالتصميم الدوار
for message in st.session_state.messages:
    align = "flex-start" if message["role"] == "user" else "flex-end"
    st.markdown(f"""
        <div style="display: flex; justify-content: {align}; width: 100%;">
            <div class="msg-card">
                <div class="msg-content">{message["content"]}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def find_any_working_model():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={NEW_API_KEY}"
    try:
        response = requests.get(url)
        models_data = response.json()
        for m in models_data.get('models', []):
            if 'generateContent' in m.get('supportedGenerationMethods', []):
                return m['name']
        return "models/gemini-1.5-flash"
    except:
        return "models/gemini-1.5-flash"

if prompt := st.chat_input("اسأل صالح AI..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# معالجة الرد
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar=None):
        with st.spinner("صالح يكتب الآن..."):
            working_model = find_any_working_model()
            url = f"https://generativelanguage.googleapis.com/v1beta/{working_model}:generateContent?key={NEW_API_KEY}"
            payload = {"contents": [{"parts": [{"text": st.session_state.messages[-1]["content"]}]}]}
            
            try:
                res = requests.post(url, json=payload)
                data = res.json()
                if res.status_code == 200:
                    ans = data['candidates'][0]['content']['parts'][0]['text']
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                    st.rerun()
                else:
                    st.error("جوجل مشغولة، جرب كمان ثانية.")
            except:
                st.error("فشل الاتصال.")
