import streamlit as st
import google.generativeai as genai

# إعدادات واجهة المستخدم
st.set_page_config(page_title="SALEH AI", page_icon="👑")

st.markdown("""
    <style>
    .main { background: #000; }
    div[data-testid="stChatMessage"] { background: #111; border: 1px solid #D4AF37; border-radius: 15px; color: #fff; }
    .stChatFloatingInputContainer { bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("👑 SALEH AI - PRO")

# إعداد المفتاح الجديد اللي بعته
API_KEY = "AIzaSyA83bkpXNvLB7bmcqOpDi7ucGYqI7K7kD4"
genai.configure(api_key=API_KEY)

# استخدام موديل مستقر جداً
model = genai.GenerativeModel('gemini-1.5-flash')

# إدارة ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة الإدخال والرد
if prompt := st.chat_input("تكلم مع صالح AI..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد رد الذكاء الاصطناعي
    with st.chat_message("assistant"):
        try:
            # استخدام أضمن طريقة للطلب
            response = model.generate_content(prompt)
            if response and response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("جوجل استلمت الطلب بس مفيش رد نصي. جرب سؤال تاني.")
        except Exception as e:
            st.error(f"حدث خطأ فني: {e}")
            st.info("لو ظهر خطأ 400 أو 403، اتأكد إن الـ API Key مفعل في منطقتك.")
