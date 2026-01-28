import streamlit as st
import requests

# --- 1. إعدادات الصفحة ---
st.set_page_config(
    page_title="SALEH AI PRO",
    page_icon="👑",
    layout="centered"
)

# --- 2. التصميم (شكل احترافي) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }
    .stApp {
        background-color: #0e1117;
    }
    h1 {
        color: #FFD700 !important;
        text-align: center;
        border-bottom: 2px solid #333;
        padding-bottom: 20px;
        text-shadow: 2px 2px 4px #000;
    }
    .stChatMessage {
        background-color: #262730;
        border-radius: 15px;
        margin-bottom: 10px;
        border: 1px solid #444;
    }
    /* لون زر الإرسال */
    .stChatInput button {
        color: #FFD700;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. الكود والمنطق ---
NEW_API_KEY = "AIzaSyAap0wkUBLjvHgmKe4sfil8FWgoc3Tfp5M"

# الدالة الأصلية مع تعديل صغير جداً لتفادي الموديل الخربان
def find_any_working_model():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={NEW_API_KEY}"
    try:
        response = requests.get(url)
        models_data = response.json()
        
        for m in models_data.get('models', []):
            name = m.get('name', '')
            
            # ⚠️ التعديل الوحيد هنا:
            # بنقوله لو اسم الموديل فيه "2.5" فكك منه وشوف غيره عشان بيعمل مشاكل
            if '2.5' in name:
                continue
                
            if 'generateContent' in m.get('supportedGenerationMethods', []):
                return name # هيرجع أول موديل شغال ومش محظور
                
        return "models/gemini-pro"
    except:
        return "models/gemini-pro"

# --- 4. الواجهة ---
with st.sidebar:
    st.title("⚙️ الإعدادات")
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

st.title("👑 SALEH AI - ULTIMATE")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = "👑" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- 5. التشغيل ---
if prompt := st.chat_input("اسأل صالح AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="👑"):
        # دالة البحث هتجيب موديل شغال وتبعد عن 2.5
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
                st.error(f"الموديل {working_model} رفض يرد (كود: {res.status_code})")
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
