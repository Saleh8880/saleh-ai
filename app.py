import streamlit as st
import requests

# --- 1. إعدادات الصفحة (نفس إعداداتك) ---
st.set_page_config(
    page_title="SALEH AI PRO",
    page_icon="👑",
    layout="centered"
)

# --- 2. التصميم الاحترافي (CSS فقط لتحسين الشكل) ---
st.markdown("""
<style>
    /* استيراد خط عربي فخم (Cairo) */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');

    /* تعميم الخط */
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }

    /* خلفية التطبيق داكنة واحترافية */
    .stApp {
        background-color: #0e1117;
    }

    /* تنسيق العنوان الرئيسي باللون الذهبي */
    h1 {
        color: #FFD700 !important;
        text-align: center;
        border-bottom: 2px solid #333;
        padding-bottom: 20px;
        text-shadow: 2px 2px 4px #000;
    }

    /* تنسيق رسائل المحادثة */
    .stChatMessage {
        background-color: #1E1E1E;
        border: 1px solid #333;
        border-radius: 15px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    }

    /* تأثير عند مرور الماوس على الرسائل */
    .stChatMessage:hover {
        border-color: #FFD700;
    }

    /* تحسين صندوق الكتابة */
    .stTextInput > div > div > input {
        border-radius: 25px;
        background-color: #262730;
        color: white;
        border: 1px solid #444;
    }
    
    /* تنسيق الزر في القائمة الجانبية */
    .stButton > button {
        width: 100%;
        background-color: #FFD700;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #FFC107;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. المتغيرات والمنطق البرمجي (النسخة الشغالة) ---
NEW_API_KEY = "AIzaSyAap0wkUBLjvHgmKe4sfil8FWgoc3Tfp5M"

# هذه الدالة كما هي في الكود الشغال بالضبط
def find_any_working_model():
    return "models/gemini-1.5-flash"

# --- 4. واجهة التطبيق ---

# القائمة الجانبية (إضافة جمالية)
with st.sidebar:
    st.title("⚙️ لوحة التحكم")
    st.markdown("---")
    st.write("📡 الحالة: **متصل**")
    st.write("🚀 الموديل: **Flash 1.5**")
    st.markdown("---")
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

# العنوان
st.title("👑 SALEH AI - ULTIMATE")

# تهيئة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    # تحديد الأيقونة: تاج للمساعد، وشخص للمستخدم
    avatar = "👑" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- 5. استقبال السؤال والمعالجة (نفس الكود الشغال) ---
if prompt := st.chat_input("اسأل صالح AI..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # الرد
    with st.chat_message("assistant", avatar="👑"):
        # عنصر نائب لعرض حالة الانتظار
        status_placeholder = st.empty()
        status_placeholder.markdown("⏳ *جاري الاتصال...*")
        
        # استدعاء الدالة المضمونة
        working_model = find_any_working_model()
        
        url = f"https://generativelanguage.googleapis.com/v1beta/{working_model}:generateContent?key={NEW_API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            res = requests.post(url, json=payload)
            
            if res.status_code == 200:
                data = res.json()
                ans = data['candidates'][0]['content']['parts'][0]['text']
                
                # مسح رسالة الانتظار وعرض الرد
                status_placeholder.empty()
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            else:
                status_placeholder.empty()
                st.error(f"⚠️ خطأ من جوجل: الموديل {working_model} لم يستجب (كود: {res.status_code})")
                
        except Exception as e:
            status_placeholder.empty()
            st.error(f"حدث خطأ برمجي: {e}")
