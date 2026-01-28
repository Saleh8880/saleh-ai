import streamlit as st
import requests

st.set_page_config(
    page_title="SALEH AI PRO",
    page_icon="👑",
    layout="centered"
)

NEW_API_KEY = "AIzaSyAap0wkUBLjvHgmKe4sfil8FWgoc3Tfp5M"

# =======================
# تنسيق الشكل فقط (CSS)
# =======================
st.markdown("""
<style>
/* خلفية عامة */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #ffffff;
    font-family: 'Cairo', sans-serif;
}

/* العنوان */
h1 {
    text-align: center;
    color: #FFD700;
    text-shadow: 0 0 10px rgba(255,215,0,0.6);
}

/* صندوق الرسائل */
.stChatMessage {
    border-radius: 15px;
    padding: 10px;
}

/* رسالة المستخدم */
[data-testid="chat-message-user"] {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255,255,255,0.15);
}

/* رسالة المساعد */
[data-testid="chat-message-assistant"] {
    background: rgba(255, 215, 0, 0.08);
    border: 1px solid rgba(255,215,0,0.3);
}

/* مربع الإدخال */
.stChatInput textarea {
    background-color: #111;
    color: #fff;
    border-radius: 12px;
    border: 1px solid #FFD700;
}

/* زر الإرسال */
.stChatInput button {
    background: linear-gradient(135deg, #FFD700, #ffae00);
    color: #000;
    border-radius: 12px;
    font-weight: bold;
}

/* سكرول بار */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: #FFD700;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("👑 SALEH AI - ULTIMATE")

# =======================
# المحادثة
# =======================
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =======================
# البحث عن موديل شغال
# =======================
def find_any_working_model():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={NEW_API_KEY}"
    try:
        response = requests.get(url)
        models_data = response.json()
        for m in models_data.get('models', []):
            if 'generateContent' in m.get('supportedGenerationMethods', []):
                return m['name']
        return "models/gemini-pro"
    except:
        return "models/gemini-pro"

# =======================
# الإدخال
# =======================
if prompt := st.chat_input("💬 اسأل صالح AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
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
                st.error(f"⚠️ الموديل {working_model} مش راضي يرد")
        except Exception as e:
            st.error(f"❌ حدث خطأ: {e}")
