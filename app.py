import streamlit as st
import requests
import time

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="SALEH AI PRO",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS للتصميم ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; }
    .stApp { background-color: #0e1117; }
    h1 { color: #FFD700 !important; text-align: center; text-shadow: 2px 2px 4px #000; }
    .stChatMessage { border-radius: 15px; padding: 10px; margin-bottom: 10px; }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) { background-color: #1f2937; border: 1px solid #374151; }
</style>
""", unsafe_allow_html=True)

# --- المفتاح ---
NEW_API_KEY = "AIzaSyAap0wkUBLjvHgmKe4sfil8FWgoc3Tfp5M"

# --- القائمة الجانبية ---
with st.sidebar:
    st.title("لوحة التحكم")
    st.success("الموديل: Gemini 1.5 Flash ⚡")
    st.info("تم تفعيل وضع التوفير لتجنب أخطاء الكوتا.")
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

st.title("👑 SALEH AI - FLASH VERSION")

# --- المحادثة ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "أهلاً! أنا جاهز وسريع جداً الآن ⚡"})

for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "👑"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- الإدخال والمعالجة ---
if prompt := st.chat_input("اسأل صالح AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="👑"):
        message_placeholder = st.empty()
        message_placeholder.markdown("⚡ *جاري الاتصال...*")
        
        # هنا التعديل المهم: نستخدم موديل فلاش مباشرة
        target_model = "models/gemini-1.5-flash"
        
        url = f"https://generativelanguage.googleapis.com/v1beta/{target_model}:generateContent?key={NEW_API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            res = requests.post(url, json=payload, timeout=10)
            
            # معالجة حالة الخطأ 429 (Too Many Requests)
            if res.status_code == 429:
                message_placeholder.error("🚨 هدي السرعة يا ريس! جوجل بيقول انتظر 30 ثانية (Quota Limit).")
            elif res.status_code == 200:
                data = res.json()
                try:
                    ans = data['candidates'][0]['content']['parts'][0]['text']
                    message_placeholder.markdown(ans)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                except:
                    message_placeholder.error("حدث خطأ في قراءة الرد.")
            else:
                message_placeholder.error(f"خطأ من جوجل: {res.status_code}")
                
        except Exception as e:
            message_placeholder.error(f"حدث خطأ: {e}")
