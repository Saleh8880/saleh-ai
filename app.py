import streamlit as st
import requests

# 1. إعدادات الصفحة والجماليات (الستايل)
st.set_page_config(page_title="SALEH AI GOLD", page_icon="👑", layout="centered")

st.markdown("""
    <style>
    /* خلفية الصفحة */
    .stApp { background: linear-gradient(to bottom, #0f0f0f, #000000); }
    
    /* شكل فقاعات الدردشة */
    div[data-testid="stChatMessage"] {
        border-radius: 20px;
        padding: 15px;
        margin-bottom: 10px;
        border: 1px solid #D4AF37; /* إطار ذهبي خفيف */
        background-color: #1a1a1a !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    /* تمييز رسالة المستخدم */
    div[data-testid="stChatMessageUser"] {
        border-right: 5px solid #D4AF37 !important;
        background-color: #262626 !important;
    }

    /* تمييز رسالة الذكاء الاصطناعي */
    div[data-testid="stChatMessageAssistant"] {
        border-left: 5px solid #ffffff !important;
    }

    /* تغيير شكل خط العناوين */
    h1 {
        color: #D4AF37;
        text-shadow: 0px 0px 10px rgba(212, 175, 55, 0.5);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
    }

    /* إخفاء علامات ستريم ليت الافتراضية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("👑 SALEH AI PRO")
st.markdown("<p style='text-align: center; color: #888;'>مساعدك الشخصي الذكي - النسخة الذهبية</p>", unsafe_allow_html=True)

# 2. المحرك (نفس الكود اللي اشتغل معاك بالظبط)
NEW_API_KEY = "AIzaSyAap0wkUBLjvHgmKe4sfil8FWgoc3Tfp5M"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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

if prompt := st.chat_input("تحدث مع صالح..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("صالح AI يكتب الآن..."):
            working_model = find_any_working_model()
            url = f"https://generativelanguage.googleapis.com/v1beta/{working_model}:generateContent?key={NEW_API_KEY}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            
            try:
                res = requests.post(url, json=payload)
                data = res.json()
                if res.status_code == 200:
                    ans = data['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(ans)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                else:
                    st.error("جوجل مشغولة شوية، حاول كمان ثواني.")
            except:
                st.error("حدث خطأ بسيط في الاتصال.")
