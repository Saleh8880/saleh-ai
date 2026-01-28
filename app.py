import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="SALEH AI PRO", page_icon="👑")

# 2. تصميمSALEH AI الدوار
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    .stApp { background-color: #000; font-family: 'Cairo', sans-serif; }
    
    /* الإطار الذهبي الدوار */
    .msg-card {
        position: relative; padding: 2px; border-radius: 15px;
        overflow: hidden; margin-bottom: 20px; width: fit-content;
        max-width: 85%;
    }
    .msg-card::before {
        content: ''; position: absolute; top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: conic-gradient(from 0deg, transparent, #D4AF37, transparent, #8A6D3B, transparent);
        animation: rotateMsg 3s linear infinite; z-index: 0;
    }
    @keyframes rotateMsg { 100% { transform: rotate(360deg); } }
    .msg-content {
        position: relative; z-index: 1; background: #0a0a0a;
        border-radius: 13px; padding: 12px 18px; color: #fff; font-size: 17px;
    }

    /* منطقة الإدخال الذهبية */
    .stChatInput div { border: 1px solid #D4AF37 !important; border-radius: 50px !important; background: #111 !important; }
    header, footer {visibility: hidden;}
    .main-title { color: #D4AF37; text-align: center; font-size: 35px; text-shadow: 0 0 15px #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">👑 SALEH AI PRO</h1>', unsafe_allow_html=True)

# 3. المحرك المباشر
API_KEY = "AIzaSyAap0wkUBLjvHgmKe4sfil8FWgoc3Tfp5M"

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل القديمة
for message in st.session_state.messages:
    align = "flex-start" if message["role"] == "user" else "flex-end"
    st.markdown(f'<div style="display: flex; justify-content: {align}; width: 100%;"><div class="msg-card"><div class="msg-content">{message["content"]}</div></div></div>', unsafe_allow_html=True)

# منطقة الإدخال والرد
if prompt := st.chat_input("اسأل صالح AI..."):
    # عرض رسالة المستخدم فوراً
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div style="display: flex; justify-content: flex-start; width: 100%;"><div class="msg-card"><div class="msg-content">{prompt}</div></div></div>', unsafe_allow_html=True)
    
    # طلب الرد من جوجل بدون تعقيد
    with st.spinner("جاري الرد..."):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        try:
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
            if res.status_code == 200:
                ans = res.json()['candidates'][0]['content']['parts'][0]['text']
                st.session_state.messages.append({"role": "assistant", "content": ans})
                # عرض رد الذكاء الاصطناعي
                st.markdown(f'<div style="display: flex; justify-content: flex-end; width: 100%;"><div class="msg-card"><div class="msg-content">{ans}</div></div></div>', unsafe_allow_html=True)
            else:
                st.error("جوجل مشغولة، جرب كمان مرة.")
        except:
            st.error("فشل الاتصال. جرب ريفريش للصفحة.")
