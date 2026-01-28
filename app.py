import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="SALEH AI PRO", page_icon="👑", layout="centered")

# 2. تصميمSALEH AI (نفس كود Colab اللي بعته)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* الخلفية الأساسية */
    .stApp { background-color: #000; font-family: 'Cairo', sans-serif; direction: rtl; }
    
    /* العنوان */
    .header-h1 { color: #D4AF37; text-align: center; font-size: 35px; text-shadow: 0 0 15px #D4AF37; margin-bottom: 20px; font-weight: bold; }

    /* حاوية الرسائل */
    .msg-card {
        position: relative; padding: 2px; border-radius: 15px;
        overflow: hidden; max-width: 85%; min-width: 120px; margin-bottom: 15px;
    }
    
    /* تأثير الإطار الذهبي الدوار */
    .msg-card::before {
        content: ''; position: absolute; top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: conic-gradient(from 0deg, transparent, #D4AF37, transparent, #8A6D3B, transparent);
        animation: rotateMsg 3s linear infinite; z-index: 0;
    }

    @keyframes rotateMsg { 100% { transform: rotate(360deg); } }

    .msg-content {
        position: relative; z-index: 1; background: #0a0a0a;
        border-radius: 13px; padding: 12px 18px; color: #fff; font-size: 16px; line-height: 1.6;
    }

    /* محاذاة الرسائل (الذكاء يمين، المستخدم يسار) */
    .stChatMessage { background-color: transparent !important; border: none !important; }
    
    /* تخصيص منطقة الإدخال */
    .stChatInputContainer { background-color: #000 !important; }
    .stChatInput div { background-color: #111 !important; border: 1px solid #333 !important; border-radius: 50px !important; }
    .stChatInput textarea { color: #fff !important; }

    /* سكرول بار ذهبي */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-thumb { background: #D4AF37; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-h1">👑 SALEH AI</div>', unsafe_allow_html=True)

# 3. المحرك الشغال (بدون تعديل في المنطق)
API_KEY = "AIzaSyAap0wkUBLjvHgmKe4sfil8FWgoc3Tfp5M"

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل بالتصميم الدوار
for message in st.session_state.messages:
    side = "user-card" if message["role"] == "user" else "ai-card"
    align = "flex-start" if message["role"] == "user" else "flex-end"
    
    st.markdown(f"""
        <div style="display: flex; justify-content: {align}; width: 100%;">
            <div class="msg-card">
                <div class="msg-content">{message["content"]}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# دالة البحث عن الموديل
def find_model():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    try:
        res = requests.get(url).json()
        for m in res.get('models', []):
            if 'generateContent' in m.get('supportedGenerationMethods', []):
                return m['name']
        return "models/gemini-1.5-flash"
    except: return "models/gemini-1.5-flash"

# منطقة الإدخال
if prompt := st.chat_input("اكتب رسالتك هنا يا صالح..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# معالجة الرد (لو آخر رسالة من المستخدم)
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner("جاري الرد..."):
        model_name = find_model()
        url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={API_KEY}"
        try:
            r = requests.post(url, json={"contents": [{"parts": [{"text": st.session_state.messages[-1]["content"]}]}]})
            if r.status_code == 200:
                ans = r.json()['candidates'][0]['content']['parts'][0]['text']
                st.session_state.messages.append({"role": "assistant", "content": ans})
                st.rerun()
            else:
                st.error("جوجل تأخرت في الرد، حاول ثانية.")
        except:
            st.error("فشل في الاتصال.")
