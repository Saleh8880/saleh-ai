import streamlit as st
import requests

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="SALEH AI PRO", page_icon="👑")

# --- 2. كود التصميم فقط (CSS) ---
# هذا الجزء لتجميل الشكل ولن يؤثر على عمل الكود
st.markdown("""
<style>
    /* استيراد خط Cairo */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }

    /* خلفية التطبيق */
    .stApp {
        background-color: #0e1117;
    }

    /* العنوان الذهبي */
    h1 {
        color: #FFD700 !important;
        text-align: center;
        border-bottom: 2px solid #333;
        padding-bottom: 20px;
        text-shadow: 2px 2px 4px #000;
    }

    /* تحسين شكل الرسائل */
    .stChatMessage {
        background-color: #262730;
        border-radius: 15px;
        border: 1px solid #333;
        margin-bottom: 10px;
    }
    
    /* تحسين صندوق الكتابة */
    .stTextInput > div > div > input {
        border-radius: 25px;
        background-color: #1E1E1E;
        color: white;
        border: 1px solid #555;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. المتغيرات والدوال (نفس كودك الأصلي بالضبط) ---

NEW_API_KEY = "AIzaSyAap0wkUBLjvHgmKe4sfil8FWgoc3Tfp5M"

st.title("👑 SALEH AI - ULTIMATE")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة (أضفت الأيقونات فقط)
for message in st.session_state.messages:
    avatar = "👑" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar): 
        st.markdown(message["content"])

# دالة للبحث عن الموديل الشغال فعلياً في حسابك (كما هي)
def find_any_working_model():
    # بنسأل جوجل عن القائمة المتاحة لك
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={NEW_API_KEY}"
    try:
        response = requests.get(url)
        models_data = response.json()
        # بنور على أي موديل بيدعم generateContent
        for m in models_data.get('models', []):
            if 'generateContent' in m.get('supportedGenerationMethods', []):
                return m['name'] # هيرجع حاجة زي models/gemini-1.5-flash-latest
        return "models/gemini-pro" # احتياطي
    except:
        return "models/gemini-pro"

# --- 4. التشغيل (نفس كودك الأصلي) ---
if prompt := st.chat_input("اسأل صالح AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="👤"): 
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="👑"):
        working_model = find_any_working_model()
        
        # نداء الموديل اللي لقيناه شغال
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
                st.error(f"جوجل لسه معاندة! الموديل اللي لقيناه هو {working_model} بس مش راضي يرد.")
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
