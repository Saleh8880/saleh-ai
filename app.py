import streamlit as st
import requests

# إعدادات الصفحة
st.set_page_config(page_title="SALEH AI PRO", page_icon="👑", layout="centered")

# الستايل اللي طلبته (الإنارة الدائرية، الخط الواضح، وزرار الإرسال)
st.markdown("""
    <style>
    /* الخلفية والإنارة الدائرية */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at center, #1a1a1a 0%, #050505 100%);
    }

    /* تحسين الخط وجعله واضح جداً */
    html, body, [class*="st-"] {
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-size: 18px;
        color: #ffffff;
    }

    /* فقاعات الكتابة بشكل جميل */
    div[data-testid="stChatMessage"] {
        background-color: rgba(30, 30, 30, 0.8) !important;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #333;
        line-height: 1.6;
    }

    /* تمييز رسالة المستخدم بلمسة ذهبية */
    div[data-testid="stChatMessageUser"] {
        border-left: 4px solid #D4AF37 !important;
    }

    /* تصميم زرار الإرسال ومنطقة الكتابة */
    .stChatInputContainer {
        padding-bottom: 30px;
    }
    
    .stChatInput textarea {
        background-color: #111 !important;
        color: white !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 10px !important;
    }

    /* العنوان مع إنارة */
    h1 {
        color: #D4AF37;
        text-align: center;
        font-size: 3rem !important;
        font-weight: 800;
        text-shadow: 0 0 20px rgba(212, 175, 55, 0.6);
        margin-bottom: 10px;
    }

    /* تخصيص الـ Spinner */
    .stSpinner > div { border-top-color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("👑 SALEH AI PRO")
st.markdown("<p style='text-align: center; color: #D4AF37; font-weight: bold;'>مساعدك الشخصي الذكي</p>", unsafe_allow_html=True)

# --- المحرك الشغال (لا يلمس) ---
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

if prompt := st.chat_input("اكتب سؤالك هنا يا صالح..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"**صالح:** {prompt}")

    with st.chat_message("assistant"):
        with st.spinner("جاري تحضير الرد..."):
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
                    st.error("جوجل مشغولة، جرب كمان ثانية.")
            except:
                st.error("فشل الاتصال.")
