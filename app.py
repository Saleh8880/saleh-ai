import streamlit as st
import google.generativeai as genai

# إعدادات واجهة صالح الذهبية
st.set_page_config(page_title="SALEH AI GOLD", page_icon="👑")

st.markdown("""
    <style>
    .main { background-color: #050505; }
    div[data-testid="stChatMessage"] { border-radius: 15px; border: 1px solid #D4AF37; color: white; }
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("👑 SALEH AI - ULTIMATE")

# مصفوفة المفاتيح (تم وضع مفاتيحك الاثنين هنا)
api_keys = [
    "AIzaSyA83bkpXNvLB7bmcqOpDi7ucGYqI7K7kD4", # المفتاح الأول
    "AIzaSyCRGxh0HeSmv0QV3BP65yMuWiltDxEskl4"  # المفتاح الثاني الجديد
]

# اختيار المفتاح الحالي
if "key_index" not in st.session_state:
    st.session_state.key_index = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# المعالجة عند الإرسال
if prompt := st.chat_input("اسأل صالح AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        success = False
        # هيجرب المفتاحين واحد ورا التاني لو حصل ضغط
        for _ in range(len(api_keys)):
            try:
                current_key = api_keys[st.session_state.key_index]
                genai.configure(api_key=current_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                success = True
                break # نجح الإرسال، اخرج من اللوب
            except Exception as e:
                if "429" in str(e): # لو المفتاح الحالي جاب Quota Exceeded
                    # بدل للمفتاح اللي بعده
                    st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
                    continue
                else:
                    st.error(f"حدث خطأ: {e}")
                    break
        
        if not success:
            st.warning("⚠️ للأسف يا صالح، المفتاحين استهلكوا كل طاقتهم حالياً. استنى دقيقة وجرب تاني.")
