# 1. تحديث المكتبة
!pip install -q -U google-generativeai

import google.generativeai as genai
from IPython.display import HTML, display
from google.colab import output

# 2. الإعدادات
API_KEY = "AIzaSyD3VJe5eS8WyZpdo98wu9MywGgbks3K2us"
genai.configure(api_key=API_KEY)

# كود ذكي لتجنب الـ 404
def find_live_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods: return m.name
    except: return 'models/gemini-1.5-flash'

model = genai.GenerativeModel(find_live_model())

# 3. الواجهة (نسخة الإصلاح النهائي)
html_code = """
<div id="saleh_root" style="background:#000; color:#fff; font-family:'Cairo', sans-serif; direction:rtl; border:2px solid #D4AF37; border-radius:15px; display:flex; flex-direction:column; height:450px;">
    
    <div style="text-align:center; padding:10px; border-bottom:1px solid #222; color:#D4AF37;">
        <h2 style="margin:0;">👑 SALEH AI - PRO</h2>
    </div>

    <div id="chat_scroll_area" style="flex:1; overflow-y:auto !important; padding:15px; display:flex; flex-direction:column; gap:15px; background:#050505;">
        <div class="ai-msg-style">أهلاً يا صالح. لو الشاشة لسه معلقة، جرب تسحب "المسطرة الذهبية" اللي على اليمين بالماوس.</div>
    </div>

    <div style="padding:10px; background:#000; border-top:1px solid #222; display:flex; gap:10px;">
        <input type="text" id="user_text_input" style="flex:1; background:#111; border:1px solid #D4AF37; color:#fff; padding:10px; border-radius:8px;" placeholder="اكتب هنا...">
        <button onclick="send_to_python()" style="background:#D4AF37; color:#000; border:none; padding:10px 20px; border-radius:8px; font-weight:bold; cursor:pointer;">إرسال</button>
    </div>
</div>

<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    .ai-msg-style { border-right:3px solid #D4AF37; padding:10px; background:#111; border-radius:8px; color:#fff; max-width:85%; align-self:flex-end; }
    .user-msg-style { border-left:3px solid #D4AF37; padding:10px; background:#D4AF37; color:#000; border-radius:8px; font-weight:bold; max-width:85%; align-self:flex-start; }
    
    /* إجبار السكرول بار على الظهور */
    #chat_scroll_area::-webkit-scrollbar { width: 12px !important; display: block !important; }
    #chat_scroll_area::-webkit-scrollbar-thumb { background: #D4AF37 !important; border-radius: 10px; border: 2px solid #000; }
    #chat_scroll_area::-webkit-scrollbar-track { background: #000 !important; }
</style>

<script>
    function send_to_python() {
        var input = document.getElementById('user_text_input');
        if(!input.value.trim()) return;
        
        drawMsg('user-msg-style', input.value);
        google.colab.kernel.invokeFunction('notebook.process_input', [input.value], {});
        input.value = '';
    }

    function drawMsg(css, txt) {
        var area = document.getElementById('chat_scroll_area');
        var div = document.createElement('div');
        div.className = css;
        div.innerHTML = txt.replace(/\\n/g, '<br>');
        area.appendChild(div);
        
        // النزول الإجباري
        area.scrollTop = area.scrollHeight;
        setTimeout(() => { area.scrollTop = area.scrollHeight; }, 200);
    }
    
    window.onAiReply = function(t) { drawMsg('ai-msg-style', t); }
</script>
"""

def process_input(text):
    try:
        response = model.generate_content(text)
        safe_reply = response.text.replace("'", "\\'").replace("\n", "<br>")
        output.eval_js(f"window.onAiReply('{safe_reply}')")
    except Exception as e:
        output.eval_js(f"window.onAiReply('خطأ: {str(e)}')")

output.register_callback('notebook.process_input', process_input)
display(HTML(html_code))
