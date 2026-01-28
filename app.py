import streamlit as st
import requests

# --- 1. إعدادات الصفحة (يجب أن تكون في البداية) ---
st.set_page_config(
    page_title="SALEH AI PRO",
    page_icon="👑",
    layout="centered"
)

# --- 2. التصميم الاحترافي (CSS) ---
st.markdown("""
<style>
    /* استيراد خط عربي أنيق */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }
    
    /* لون الخلفية ونمط الرسائل */
    .stApp {
        background-color: #0e1117;
    }
    
    h1 {
        color: #FFD700 !important; /* لون ذهبي */
        text-align: center;
        border-bottom: 1px solid #333;
        padding-bottom: 20px;
    }
    
    /* تحسين شكل الرسائل */
    .stChatMessage {
        background-color: #262730;
        border-radius: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. المتغيرات والدوال (من كودك الشغال) ---
NEW_API_KEY = "AIzaSyAap0wkUBLjvHgmKe4sfil8FWgoc3Tfp5M"

def find_any_working_model():
    # دالتك الأصلية التي تعمل بنجاح
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

# --- 4. واجهة التطبيق ---

# القائمة الجانبية (إضافة جمالية)
with st.sidebar:
    st.title("⚙️ لوحة التحكم")
    st.write("حالة النظام: **متصل** ✅")
    if st.button("مسح المحادثة 🗑️"):
        st.session_state.messages = []
        st.rerun()

st.title("👑 SALEH AI - ULTIMATE")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة السابقة
for message in st.session_state.messages:
    # تحديد الأيقونة بناءً على المرسل
    avatar = "👑" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- 5. استقبال السؤال والمعالجة ---
if prompt := st.chat_input("اسأل صالح AI..."):
    # عرض سؤال المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # معالجة الرد
    with st.chat_message("assistant", avatar="👑"):
        status_placeholder = st.empty()
        status_placeholder.markdown("⏳ *جاري الاتصال بالموديل...*")
        
        working_model = find_any_working_model()
        
        # استخدام نفس رابطك ومنطقك
        url = f"https://generativelanguage.googleapis.com/v1beta/{working_model}:generateContent?key={NEW_API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            res = requests.post(url, json=payload)
            data = res.json()

            if res.status_code == 200:
                # نجح الاتصال
                ans = data['candidates'][0]['content']['parts'][0]['text']
                status_placeholder.empty() # إخفاء رسالة الانتظار
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            else:
                status_placeholder.empty()
                st.error(f"⚠️ خطأ من جوجل: {working_model} لم يستجب. (Code: {res.status_code})")
                
        except Exception as e:
            status_placeholder.empty()
            st.error(f"حدث خطأ برمجي: {e}")
