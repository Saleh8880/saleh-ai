import streamlit as st
import requests

# --- 1. إعدادات الصفحة ---
st.set_page_config(
    page_title="SALEH AI PRO",
    page_icon="👑",
    layout="wide", # جعلته wide لاستغلال الشاشة بشكل أفضل
    initial_sidebar_state="expanded"
)

# --- 2. التصميم الاحترافي الفاخر (CSS) ---
st.markdown("""
<style>
    /* استيراد خط عربي عصري (Cairo) */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;500;700&display=swap');

    /* تطبيق الخط على كل شيء */
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }

    /* خلفية التطبيق: تدرج لوني داكن فخم */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        background-attachment: fixed;
    }

    /* الشريط الجانبي */
    section[data-testid="stSidebar"] {
        background-color: rgba(17, 25, 40, 0.75);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 215, 0, 0.1);
    }

    /* العنوان الرئيسي */
    h1 {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 700;
        text-shadow: 0px 4px 10px rgba(0,0,0,0.5);
        padding-bottom: 20px;
    }

    /* تصميم رسائل الشات (Glassmorphism) */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
        border: 1px solid rgba(255, 215, 0, 0.3); /* توهج ذهبي خفيف عند المرور */
    }

    /* تحسين شكل الأكواد داخل الشات */
    code {
        color: #e0e0e0;
        background-color: #1a1a1a;
        border-radius: 5px;
    }

    /* تحسين صندوق الكتابة (Input) */
    .stTextInput > div > div > input {
        background-color: rgba(0, 0, 0, 0.3);
        color: white;
        border-radius: 30px;
        border: 1px solid #444;
        padding: 10px 20px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #FFD700;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
    }

    /* تنسيق زر القائمة الجانبية */
    .stButton > button {
        background: linear-gradient(45deg, #FFD700, #FFC107);
        color: black;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
    }

    /* إخفاء القائمة العلوية الافتراضية لـ Streamlit لمظهر أنظف */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# --- 3. المتغيرات والدالة (نفس الكود الشغال) ---
NEW_API_KEY = "AIzaSyAap0wkUBLjvHgmKe4sfil8FWgoc3Tfp5M"

def find_any_working_model():
    # نفس الدالة الشغالة المثبتة على الفلاش
    return "models/gemini-1.5-flash"

# --- 4. الشريط الجانبي (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #FFD700;'>⚙️ إعدادات المساعد</h2>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        st.write("🟢")
    with col2:
        st.write("**الحالة:** متصل بالخوادم")
        
    st.caption(f"🚀 الموديل: Gemini 1.5 Flash")
    
    st.write("---")
    st.info("💡 **تلميح:** هذا الموديل سريع جداً ومخصص للإجابات المباشرة.")
    
    st.write("---")
    if st.button("🗑️ بدء محادثة جديدة"):
        st.session_state.messages = []
        st.rerun()

# --- 5. واجهة المحادثة الرئيسية ---

# عنوان بتأثير إيموجي كبير
col_main_1, col_main_2 = st.columns([1, 10])
with col_main_1:
    st.image("https://cdn-icons-png.flaticon.com/512/6134/6134346.png", width=60) # أيقونة تاج
with col_main_2:
    st.title("SALEH AI - ULTIMATE")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل
for message in st.session_state.messages:
    # تخصيص الأيقونات
    if message["role"] == "assistant":
        avatar = "https://cdn-icons-png.flaticon.com/512/4712/4712035.png" # صورة روبوت/تاج
    else:
        avatar = "https://cdn-icons-png.flaticon.com/512/9187/9187604.png" # صورة مستخدم أنيقة
        
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- 6. الإدخال والمعالجة ---
if prompt := st.chat_input("اكتب رسالتك للملك صالح..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="https://cdn-icons-png.flaticon.com/512/9187/9187604.png"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="https://cdn-icons-png.flaticon.com/512/4712/4712035.png"):
        status_box = st.empty()
        # تأثير انتظار جميل
        status_box.markdown("""
            <div style='display: flex; align-items: center; gap: 10px;'>
                <span style='font-size: 20px;'>⚡</span>
                <span style='color: #FFD700;'>جاري التحليل والمعالجة...</span>
            </div>
        """, unsafe_allow_html=True)
        
        working_model = find_any_working_model()
        url = f"https://generativelanguage.googleapis.com/v1beta/{working_model}:generateContent?key={NEW_API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            res = requests.post(url, json=payload)
            
            if res.status_code == 200:
                data = res.json()
                ans = data['candidates'][0]['content']['parts'][0]['text']
                status_box.empty()
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            else:
                status_box.empty()
                st.error(f"⚠️ خطأ تقني: {res.status_code}")
                
        except Exception as e:
            status_box.empty()
            st.error(f"حدث خطأ: {e}")
