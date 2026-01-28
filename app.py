import streamlit as st
import requests

# --- 1. إعدادات الصفحة ---
st.set_page_config(
    page_title="SALEH AI PRO",
    page_icon="👑",
    layout="centered"
)

# --- 2. التصميم (CSS فقط - لن يؤثر على الكود البرمجي) ---
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
    
    /* عند مرور الماوس على الرسالة */
    .stChatMessage:hover {
        border-color: #FFD700;
    }

    /* تحسين صندوق الكتابة */
    .stTextInput > div > div > input {
        border-radius: 25px;
        background-color: #1E1E1E;
        color: white;
        border: 1px solid #555;
    }
    .stTextInput > div > div > input:focus {
        border-color: #FFD700;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. الكود البرمجي الأصلي (كما هو) ---

NEW_API_KEY = "AIzaSyAap0wkUBLjvHgmKe4sfil8FWgoc3Tfp5M"

# هذه دالتك الأصلية التي تبحث في القائمة (لم أغيرها)
def find_any_working_model():
    # بنسأل جوجل عن القائمة المتاحة لك
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={NEW_API_KEY}"
    try:
        response = requests.get(url)
        models_data = response.json()
        # بندور على أي موديل بيدعم generateContent
        for m in models_data.get('models', []):
            if 'generateContent' in m.get('supportedGenerationMethods', []):
                return m['name'] # هيرجع اسم الموديل الصحيح من القائمة
        return "models/gemini-pro" # احتياطي
    except:
        return "models/gemini-pro"

# --- 4. الواجهة والعرض ---

# القائمة الجانبية (إضافة للتصميم فقط)
with st.sidebar:
    st.title("⚙️ الإعدادات")
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.write("---")
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

st.title("👑 SALEH AI - ULTIMATE")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    # أيقونات للتجميل
    avatar = "👑" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar): 
        st.markdown(message["content"])

# --- 5. التشغيل (نفس كودك الأصلي) ---
if prompt := st.chat_input("اسأل صالح AI..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="👤"): 
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="👑"):
        # عنصر لعرض حالة الانتظار بشكل جميل
        status = st.empty()
        status.markdown("⏳ *جاري الاتصال...*")

        working_model = find_any_working_model()
        
        # نداء الموديل
        url = f"https://generativelanguage.googleapis.com/v1beta/{working_model}:generateContent?key={NEW_API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            res = requests.post(url, json=payload)
            data = res.json()
            
            if res.status_code == 200:
                try:
                    ans = data['candidates'][0]['content']['parts'][0]['text']
                    status.empty() # إخفاء كلمة جاري الاتصال
                    st.markdown(ans)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                except:
                    status.empty()
                    st.error("وصل رد فارغ أو غير مفهوم من جوجل.")
            else:
                status.empty()
                st.error(f"جوجل لسه معاندة! الموديل اللي لقيناه هو {working_model} بس مش راضي يرد. (كود: {res.status_code})")
                
        except Exception as e:
            status.empty()
            st.error(f"حدث خطأ: {e}")
