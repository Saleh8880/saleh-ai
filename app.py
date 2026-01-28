import streamlit as st
import requests

# --- إعدادات الصفحة (يجب أن تكون أول أمر) ---
st.set_page_config(
    page_title="SALEH AI PRO",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- تنسيق CSS مخصص لتحسين المظهر (نمط داكن واحترافي) ---
st.markdown("""
<style>
    /* استيراد خط عربي جميل (Cairo) */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');

    /* تطبيق الخط على كامل التطبيق */
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }

    /* خلفية التطبيق */
    .stApp {
        background-color: #0e1117;
    }

    /* تنسيق العنوان الرئيسي */
    h1 {
        color: #FFD700 !important; /* لون ذهبي */
        text-align: center;
        text-shadow: 2px 2px 4px #000000;
        padding-bottom: 20px;
        border-bottom: 2px solid #333;
    }

    /* تنسيق صندوق المحادثة */
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    
    /* رسائل المستخدم */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #1f2937;
        border: 1px solid #374151;
    }

    /* زر الإرسال وصندوق الكتابة */
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 1px solid #FFD700;
    }
</style>
""", unsafe_allow_html=True)

# --- المتغيرات والثوابت ---
# ⚠️ تحذير: يُفضل عدم وضع مفتاح API مباشرة في الكود عند النشر
NEW_API_KEY = "AIzaSyAap0wkUBLjvHgmKe4sfil8FWgoc3Tfp5M"

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100) # صورة رمزية
    st.title("لوحة التحكم")
    st.info("مرحباً بك في النسخة الاحترافية من Saleh AI.")
    st.markdown("---")
    st.write("🔧 **حالة النظام:** متصل")
    st.write("🚀 **الموديل:** Auto-Detect")
    st.markdown("---")
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

# --- العنوان الرئيسي ---
st.title("👑 SALEH AI - ULTIMATE")
st.caption("🚀 مساعدك الذكي المتطور المدعوم بتقنيات Google Gemini")

# --- إدارة حالة الجلسة ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # رسالة ترحيبية أولية
    st.session_state.messages.append({"role": "assistant", "content": "مرحباً يا زعيم! 👑 كيف يمكنني مساعدتك اليوم؟"})

# --- عرض المحادثة ---
for message in st.session_state.messages:
    # تحديد الأيقونات بناءً على الدور
    avatar = "👤" if message["role"] == "user" else "👑"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- دالة البحث عن الموديل (مع كاشينج لتحسين الأداء) ---
@st.cache_data(show_spinner=False)
def find_working_model():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={NEW_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return "models/gemini-pro"
            
        models_data = response.json()
        # نفضل gemini-1.5-flash لسرعته، ثم pro
        preferred_models = ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]
        
        available_models = [m['name'] for m in models_data.get('models', []) if 'generateContent' in m.get('supportedGenerationMethods', [])]
        
        # البحث عن المفضل أولاً
        for pref in preferred_models:
            for avail in available_models:
                if pref in avail:
                    return avail
                    
        # إذا لم نجد المفضل، نأخذ أول واحد متاح
        if available_models:
            return available_models[0]
            
        return "models/gemini-pro"
    except:
        return "models/gemini-pro"

# --- معالجة الإدخال ---
if prompt := st.chat_input("اكتب سؤالك هنا..."):
    # إضافة سؤال المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # معالجة الرد
    with st.chat_message("assistant", avatar="👑"):
        message_placeholder = st.empty()
        message_placeholder.markdown("⏳ *جاري التفكير...*")
        
        working_model = find_working_model()
        
        url = f"https://generativelanguage.googleapis.com/v1beta/{working_model}:generateContent?key={NEW_API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            res = requests.post(url, json=payload, timeout=10)
            data = res.json()
            
            if res.status_code == 200:
                try:
                    ans = data['candidates'][0]['content']['parts'][0]['text']
                    message_placeholder.markdown(ans)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                except (KeyError, IndexError):
                    message_placeholder.error("عذراً، لم أتمكن من قراءة الرد. حاول صياغة السؤال بطريقة أخرى.")
            else:
                error_msg = data.get('error', {}).get('message', 'Unknown Error')
                message_placeholder.error(f"خطأ في الاتصال: {error_msg}")
                
        except Exception as e:
            message_placeholder.error(f"حدث خطأ غير متوقع: {e}")

