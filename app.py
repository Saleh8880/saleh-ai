import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="SALEH AI PRO", page_icon="👑", layout="centered")

# 2. تصميمSALEH AI (الإطارات الدوارة الموحدة)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    .stApp { background-color: #000; font-family: 'Cairo', sans-serif; }
    
    .header-h1 { 
        color: #D4AF37; text-align: center; font-size: 32px; 
        text-shadow: 0 0 15px #D4AF37; margin-bottom: 20px; font-weight: 700; 
    }

    /* تأثير المربع الذهبي الدوار */
    .msg-card {
        position: relative; padding: 2px; border-radius: 15px;
        overflow: hidden; margin-bottom: 15px; width: fit-content;
        max-width: 85%; min-width: 120px;
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
        border-radius: 13px; padding: 12px 18px; color: #fff; font-size: 16px;
    }

    /* تنسيق منطقة الإدخال لتبدو مثل التصميم المطلوب */
    .stChatInputContainer { padding-bottom: 30px !important; }
    .stChatInput div { border: 1px solid #D4AF37 !important; border-radius: 50px !important; background: #111 !important; }
    
    /* إخفاء أيقونات ستريم ليت */
    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-h1">👑 SALEH AI</div>', unsafe_allow_html=True)

# 3. المحرك المباشر (الأكثر استقراراً)
API_KEY = "AIzaSyAap0wkUBLjvHgmKe4sfil8FWgoc3Tfp5M"

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الشات
for message in st.session_state.messages:
    align = "flex-start" if message["role"] == "user" else "flex-end"
    st.markdown(f"""
        <div style="display: flex; justify-content: {align}; width: 100%; direction: rtl;">
            <div class="msg-card">
                <div class="msg-content">{message["content"]}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# دالة ذكية لإحضار الموديل الشغال
def get_working_url():
    # بنجرب الموديل الأكثر استقراراً مباشرة
    return f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

if prompt := st.chat_input("اكتب هنا يا صالح..."):
    # إضافة رسالة المستخدم فوراً
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # محاكاة الرد فوراً بدون rerun معقدة
    with st.chat_message("assistant", avatar=None):
        url = get_working_url()
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            res = requests.post(url, json=payload, timeout=15)
            if res.status_code == 200:
                ans = res.json()['candidates'][0]['content']['parts'][0]['text']
                st.session_state.messages.append({"role": "assistant", "content": ans})
                st.rerun()
            else:
                # محاولة بديلة بموديل برو لو فلاش فشل
                url_pro = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
                res = requests.post(url_pro, json=payload, timeout=15)
                if res.status_code == 200:
                    ans = res.json()['candidates'][0]['content']['parts'][0]['text']
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                    st.rerun()
                else:
                    st.error("جوجل مشغولة، جرب كمان ثواني.")
        except:
            st.error("فشل الاتصال، تأكد من مفتاح الـ API أو اتصال الإنترنت.")
