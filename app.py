import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from utils import format_gold_weight, calculate_pe, format_length_inches, to_pe
import logic
import google.generativeai as genai

st.markdown("""
    <style>
    /* ၁။ App တစ်ခုလုံး၏ နောက်ခံနှင့် Theme */
    .stApp {
        background-color: #2F1B05 !important;
        color: #D4AF37 !important;
    }

    /* ၂။ Sidebar နောက်ခံကို အညိုရင့်ရောင်နှင့် ရွှေရောင်ဘောင်သတ်ခြင်း */
    [data-testid="stSidebar"] {
        background-color: #1E1103 !important;
        border-right: 2px solid #D4AF37 !important;
    }

    /* ၃။ Sidebar Menu ကို Card ပုံစံပြောင်းခြင်း (Hover Effect ပါဝင်သည်) */
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        background-color: #3D2307 !important;
        border: 1.5px solid #D4AF37 !important;
        padding: 12px 15px !important;
        border-radius: 12px !important;
        color: #D4AF37 !important;
        margin-bottom: 10px !important;
        display: flex !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.5) !important;
    }

    /* ရွေးချယ်ထားသော Card ကို ရွှေရောင်တောက်စေခြင်း */
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-selected="true"] {
        background-color: #D4AF37 !important;
        color: #000000 !important;
        font-weight: bold !important;
        box-shadow: 0px 0px 18px rgba(212, 175, 55, 0.7) !important;
        transform: scale(1.02);
    }

    /* ၄။ Sidebar ဖွင့်/ပိတ် ခလုတ်များ (Glow Effect ပါသော ရွှေရောင်အဝိုင်း) */
    button[data-testid="stSidebarCollapseButton"], 
    header[data-testid="stHeader"] button {
        background-color: #D4AF37 !important;
        color: black !important;
        border-radius: 50% !important;
        border: 2px solid white !important;
        width: 45px !important;
        height: 45px !important;
        box-shadow: 0px 0px 15px rgba(212, 175, 55, 0.8) !important;
    }
    button svg { fill: black !important; }

    /* ၅။ AI Chat (အမရာ) နှင့် စာသားများ အားလုံးကို ထင်ရှားစေခြင်း */
    [data-testid="stChatMessage"] p, [data-testid="stMarkdownContainer"] p, .stWidgetLabel p, .stAlert p {
        color: #D4AF37 !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.9) !important; /* စာသားများ ထင်ရှားစေရန် အရိပ်ထည့်ခြင်း */
    }
    
    [data-testid="stChatMessage"] {
        background-color: #3D2307 !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 15px !important;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3) !important;
    }

    /* ၆။ ခေါင်းစဉ်များကို ကနုတ်ရိုးရာဆန်ဆန် ရွှေရောင်လင်းစေခြင်း */
    h1, h2, h3 {
        color: #D4AF37 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7) !important;
        letter-spacing: 1px;
    }

    /* ၇။ Input Boxes & Number Fields (ရိုက်ထည့်လိုက်သော ဂဏန်းများ ထင်ရှားစေရန်) */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #3D2307 !important;
        color: #FFD700 !important; /* ပိုလင်းသော ရွှေဝါရောင် */
        border: 1px solid #D4AF37 !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }

    /* ၈။ မူလ Radio Button အဝိုင်းလေးများကို ဖျောက်ထားခြင်း */
    [data-testid="stSidebar"] div[role="radiogroup"] [data-testid="stWidgetSelectionStateColumn"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# API Key ကို Streamlit Secrets မှ ခေါ်ယူခြင်း
api_key = st.secrets["GOOGLE_API_KEY"]

# Google Analytics အလုပ်လုပ်စေမည့် ကုဒ်
ga_code = """
<script async src="https://wwwwgoogletagmanager.com/gtag/js?id=G-HQ8THB6NQ4"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-HQ8THB6NQ4');
</script>
"""
# အပေါ်က G-XXXXXXXXXX နှစ်နေရာလုံးကို အစ်ကို့ ID နဲ့ အစားထိုးပါ
st.components.v1.html(ga_code, height=0)

def format_weight(k, p, y, pt):
    parts = []
    if k > 0: parts.append(f"{k} ကျပ်")
    if p > 0: parts.append(f"{p} ပဲ")
    if y > 0: parts.append(f"{y} ရွေး")
    if pt > 0: parts.append(f"{pt} Pt")
    return " ".join(parts) if parts else "0"

def init_db():
    conn = sqlite3.connect('jewelry_records.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS receipts 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  date TEXT, 
                  customer_name TEXT, 
                  details TEXT, 
                  total_weight TEXT)''')
    conn.commit()
    conn.close()

init_db() # App စတက်တာနဲ့ Database အသင့်ဖြစ်အောင် လုပ်ထားပါ

st.set_page_config(page_title="မြန်မာ့ရွှေပန်းတိမ်သုံး", page_icon="⚒️", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #1a1a1a; /* အနက်ရောင်နောက်ခံ */
        color: #D4AF37; /* ရွှေရောင်စာသား */
    }
    div.stButton > button {
        background-color: #D4AF37;
        color: black;
        border-radius: 10px;
        border: 2px solid #D4AF37;
    }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #D4AF37;'>လုပ်ဆောင်ချက်များ</h2>", unsafe_allow_html=True)
    
    menu_options = [
        "🏠 ပင်မ စာမျက်နှာ",
        "အမရာ - AI လက်ထောက်",
        "💰 ရွှေ မှ ငွေ",
        "ငွေမှ ရွှေတွက်ရန်",
        "📐 အချိုးအစားတွက်စက်",
        "💍 လက်စွပ်/လက်ကောက်",
        "📋 အထည်ယူ/အထည်အပ်",
        "💎 စိန်/ကျောက်/ပုလဲ (အထည်ယူ/အပ်)",
        "💎 3D ဖယောင်းတွက်စက်",
        "Gram မှ ကျပ်/ပဲ/ရွေး ပြောင်းရန်",
        "ကာရက်မှ ရတီဈေးနှုန်းတွက်ချက်ရန်"

    ]
    
    menu = st.radio("", menu_options, label_visibility="collapsed")
  
    st.markdown("---") # နောက်ထပ် မျဉ်းကြောင်း

    # ၃။ လိပ်စာနှင့် ဖုန်းနံပါတ်ကို Icon လေးများနှင့် ထည့်ခြင်း
    st.markdown("""
        <div style='text-align: center; color: #aaa; font-size: 14px;'>
        <b>App by MinThitsarAung</b><br>
        📞 09777429848
        </div>
    """, unsafe_allow_html=True)

if menu == "🏠 ပင်မ စာမျက်နှာ":
    st.markdown("<h1 style='text-align: center; color: #D4AF37;'>✨ မြန်မာ့ရွှေပန်းတိမ်သုံး</h1>", unsafe_allow_html=True)

elif menu == "အမရာ - AI လက်ထောက်":
    st.title("🤖 အမရာ - ကိုမင်းသစ္စာအောင်ရဲ့ လက်ထောက် AI")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # စကားပြောခန်း (Chat interface)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("အမရာကို မေးပါ..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            history = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages[:-1]]
            response_text = logic.get_amara_response(prompt, history, api_key)
            st.write(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
          
elif menu == "💰 ရွှေ မှ ငွေ":
    st.header("💰 ရွှေ နှင့် ငွေ လဲလှယ်ခြင်း")
    gold_price = st.number_input("ယနေ့ အခေါက်ရွှေဈေး (၁ ကျပ်သား):", value=10900000)
    
    st.markdown("---")
    st.subheader("⚖️ ရွှေမှ ငွေသို့ တွက်ချက်ရန်")

    # ၁။ ရွှေအလေးချိန် ထည့်ရန်
    st.write("**၁။ ရွှေအလေးချိန် ထည့်ပါ**")
    k, p, y, pt = st.columns(4)
    gk = k.number_input("ကျပ်", min_value=0, key="gk")
    gp = p.number_input("ပဲ", min_value=0, max_value=15, key="gp")
    gy = y.number_input("ရွေး", min_value=0, max_value=7, key="gy")
    gpt = pt.number_input("Pt", min_value=0, max_value=9, key="gpt")
    
    # ၂။ အလျော့တွက် ထည့်ရန်
    st.write("**၂။ နှုတ်မည့် အလျော့တွက် ထည့်ပါ**")
    wk, wp, wy, wpt = st.columns(4)
    awk = wk.number_input("ကျပ်", min_value=0, key="awk")
    awp = wp.number_input("ပဲ", min_value=0, max_value=15, key="awp")
    awy = wy.number_input("ရွေး", min_value=0, max_value=7, key="awy")
    awpt = wpt.number_input("Pt", min_value=0, max_value=9, key="awpt")
    
    # ၃။ ပဲရည်နှင့် တွက်ချက်ရန် (ပဲရည် ၁၂ ထည့်ထားပါတယ်)
    st.write("**၃။ ပဲရည်ရွေးချယ်ပြီး တွက်ချက်ပါ**")
    c1, c2 = st.columns([2, 1])
    with c1:
        # ဒီနေရာမှာ ၁၂ ကို ထပ်တိုးထားပါတယ်
        pur = st.selectbox("ပဲရည်:", [16, 15, 14.2, 14, 13, 12], key="p1", label_visibility="collapsed")
    with c2:
        calc_btn = st.button("တွက်ချက်မည်", use_container_width=True)

    if calc_btn:
        cost = logic.gold_to_money(gk, gp, gy, gpt, awk, awp, awy, awpt, gold_price, pur)
        
        st.markdown(f"""
            <div style='border: 2px solid #D4AF37; padding: 20px; border-radius: 15px; text-align: center; background-color: #FFF9E3; margin-top: 20px;'>
                <p style='color: #5D4037; font-size: 18px; margin-bottom: 5px;'>စုစုပေါင်း ကျသင့်ငွေ ({pur} ပဲရည်)</p>
                <h2 style='color: #B22222; margin: 0;'>{int(cost):,} ကျပ်</h2>
            </div>
        """, unsafe_allow_html=True)
      
elif menu == "Gram မှ ကျပ်/ပဲ/ရွေး ပြောင်းရန်":
    st.title("Gram မှ ကျပ်/ပဲ/ရွေးသို့ ပြောင်းရန်")
    
    # User ဆီက input တောင်းခြင်း
    grams = st.number_input("ဂရမ် (Gram) ထည့်ပါ", value=0.0)
    system_type = st.radio("စနစ်ရွေးချယ်ပါ", ("စနစ်ဟောင်း (16.606g)", "စနစ်သစ် (16.329g)"))
    
    # logic.py ထဲက Function ကို ခေါ်သုံးခြင်း
    if grams > 0:
        if system_type == "စနစ်ဟောင်း (16.606g)":
            result = logic.convert_old_system(grams)
        else:
            result = logic.convert_new_system(grams)
          # app.py တွင်
    if st.button("တွက်ချက်ရန်"):  # ခလုတ်ထည့်ခြင်း
       if grams > 0:
          divisor = 16.606 if system_type == "စနစ်ဟောင်း (16.606g)" else 16.329
          result = logic.convert_gold(grams, divisor)
          st.success(f"ရလဒ်မှာ - {result} ဖြစ်ပါသည်။")

elif menu == "📐 အချိုးအစားတွက်စက်":
    st.subheader("📐 အချိုးအစားနှင့် ရွှေချိန်တွက်ချက်မှုများ")
    
    st.subheader("⚖️ ၁။ ရွှေချိန် ပေါင်း/နုတ်")
    r_col1, r_col2 = st.columns(2)
    with r_col1:
        st.write("ပထမ ရွှေချိန်")
        k1, p1, y1, pt1 = st.number_input("ကျပ်(1)", 0, key="ak1"), st.number_input("ပဲ(1)", 0, 15, key="ap1"), st.number_input("ရွေး(1)", 0, 7, key="ay1"), st.number_input("Pt(1)", 0.0, step=0.1, key="apt1")
    with r_col2:
        st.write("ဒုတိယ ရွှေချိန်")
        k2, p2, y2, pt2 = st.number_input("ကျပ်(2)", 0, key="bk1"), st.number_input("ပဲ(2)", 0, 15, key="bp1"), st.number_input("ရွေး(2)", 0, 7, key="by1"), st.number_input("Pt(2)", 0.0, step=0.1, key="bpt2")
        
    if st.button("ပေါင်း/နုတ် တွက်ရန်"):
        res_add = logic.gold_addition(k1, p1, y1, pt1, k2, p2, y2, pt2)
        res_sub = logic.gold_subtraction(k1, p1, y1, pt1, k2, p2, y2, pt2)
        st.success(f"➕ ပေါင်းလဒ်: {res_add['kyat']} ကျပ် {res_add['pae']} ပဲ {res_add['yway']} ရွေး {res_add['point']} Pt")
        if res_sub:
            st.warning(f"➖ အနုတ်လဒ်: {res_sub['kyat']} ကျပ် {res_sub['pae']} ပဲ {res_sub['yway']} ရွေး {res_sub['point']} Pt")
        else:
            st.error("⚠️ အနုတ်လဒ်: ပထမရွှေချိန် နည်းနေပါသည်။")

    st.write("---")
    st.subheader("⚖️ ၂။ လက်မအလိုက် ရွှေအလေးချိန်")
    ca, cb, cc = st.columns(3)
    i_val = ca.number_input("အရှည်(လက်မ)", value=1.0, step=0.1, key="inch_in")
    y_val = cb.number_input("၁လက်မစာ (ရွေး)", 0, 7, key="yway_in")
    pt_val = cc.number_input("၁လက်မစာ (Point)", 0.0, 9.9, step=0.1, key="pt_in")
    
    if st.button("လက်မအလိုက် တွက်ရန်"):
        # logic.py ထဲက function အသစ်ကို လှမ်းခေါ်ခြင်း
        res = logic.weight_per_inch_comprehensive(i_val, y_val, pt_val)
        
        st.markdown(f"""
            <div class='kanote-border'>
                <h4 style='color: #D4AF37;'>စုစုပေါင်း ရွှေအလေးချိန်</h4>
                <p style='font-size: 22px;'>
                    <b>{res['kyat']} ကျပ် {res['pae']} ပဲ {res['yway']} ရွေး {res['point']} Point</b>
                </p>
                <p style='color: #888;'>စုစုပေါင်း Point: {res['total_pts']}</p>
            </div>
        """, unsafe_allow_html=True)

    st.write("---")
    st.subheader("📏 ၄။ အချိုးကျ အလျားမြှောက်စက်")
    st.info("ဥပမာ - ၁ လက်မလျှင် ၇ လက်မနှုန်းဖြင့် လက်မ ၂၀ အတွက် တွက်ချက်ခြင်း")
    
    col_x, col_y = st.columns(2)
    with col_x:
        target_in = st.number_input("မူလ လက်မ (ဥပမာ-၂၀)", value=20.0, key="target_multi")
    with col_y:
        ratio_val = st.number_input("အချိုး (ဥပမာ-၇)", value=7.0, key="ratio_multi")
        
    if st.button("အလျားမြှောက်ရန်"):
        res = logic.calculate_ratio_multiplication(target_in, ratio_val)
        st.markdown(f"""
            <div class='kanote-border'>
                <h4>တွက်ချက်မှု ရလဒ်</h4>
                <p style='font-size: 25px; color: #D4AF37;'>
                    <b>{res['feet']} ပေ {res['inches']} လက်မ</b>
                </p>
                <p>စုစုပေါင်းလက်မ: {res['total_in']} inch</p>
            </div>
        """, unsafe_allow_html=True)
  
    st.write("---")
    st.subheader("📏 ၃။ အလျားမြှောက်စက် (အလီ)")
    la, lb, lc = st.columns(3)
    l_in = la.number_input("လက်မ", 6, key="l_in")
    b_sel = lb.selectbox("ပဲ", list(range(16)), key="b_sel")
    a_in = lc.number_input("အလီ", 3, key="ali_in")
    
    if st.button("အလီ တွက်ရန်"):
        total_l = logic.length_multiplier_ali(l_in, b_sel, a_in)
        st.write(f"ရလဒ်: {total_l}")



elif menu == "💍 လက်စွပ်/လက်ကောက်":
    st.subheader("💍 လက်စွပ် နှင့် လက်ကောက် တိုင်းတာခြင်း")
   import logic # logic.py ကို ချိတ်ဆက်ရန်

st.title("💍 လက်စွပ်/လက်ကောက် အတိုင်းအတာ")

# လက်စွပ်နံပါတ် ရိုက်ထည့်ခြင်း
size_input = st.number_input("လက်စွပ်နံပါတ် ရိုက်ထည့်ပါ (ဥပမာ- ၁၂)", min_value=10, max_value=25, value=12)

# Logic ဖိုင်မှ အဖြေကို ယူခြင်း
result = logic.get_ring_data_by_size(size_input)

if result:
    st.markdown(f"""
    <div style="background-color: #3D2307; padding: 20px; border-radius: 15px; border: 1px solid #FFD700;">
        <h4 style="color: #FFD700; margin: 0;">✅ အတိုင်းအတာ ရလဒ်</h4>
        <p style="font-size: 18px; color: #FFD700; margin-top: 10px;">
            Size <b>{size_input}</b> ၏ ပတ်လည်မှာ <b>{result['mm']} mm</b> ဖြစ်ပါသည်။
        </p>
        <p style="font-size: 22px; color: #FFD700; font-weight: bold;">
            📏 မြန်မာလို အတိုင်းအတာ- <span style="color: #FFF;">{result['inches']} လက်မ နှင့် {result['pae']} ပဲ</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("⚠️ ဤနံပါတ်အတွက် အချက်အလက် မရှိသေးပါ။")
elif menu == "📋 အထည်ယူ/အထည်အပ်":
    st.markdown("<h2 style='text-align: center;'>📋 အထည်ယူ နှင့် အထည်အပ် စာရင်း</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📥 အထည်ယူ (စာရင်းသွင်း)", "📤 အထည်အပ် (တွက်ချက်မှု)"])
    
    with tab1:
        st.subheader("📥 အထည်လက်ခံဖြတ်ပိုင်း")
        item_name = st.text_input("အထည်အမည်", placeholder="ဥပမာ - ဟန်ဒီကြိုး")
        target_w = st.text_input("ပြုလုပ်ရမည့် အလေးချိန်", placeholder="၁ကျပ် ၂ပဲ")
        target_l = st.text_input("ပြုလုပ်ရမည့် အရှည်", placeholder="၁၈ လက်မ")
        
        st.write("---")
        st.write("💰 **ပေးရွှေ**")
        gk, gp, gy, gpt = st.columns(4)
        g_k = gk.number_input("ကျပ်", 0, key="take_k")
        g_p = gp.number_input("ပဲ", 0, 15, key="take_p")
        g_y = gy.number_input("ရွေး", 0, 7, key="take_y")
        g_pt = gpt.number_input("Point", 0.0, 9.9, key="take_pt")
        
        note1 = st.text_area("မှတ်ချက်", key="note_take")
        
        if st.button("ယူသည့်ပြေစာ ထုတ်ရန်"):
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            st.markdown(f"""
                <div style="background: #0a0a0a; border: 2px solid #D4AF37; padding: 30px; border-radius: 10px; color: white; font-family: 'Pyidaungsu', sans-serif; box-shadow: 0px 0px 15px rgba(212, 175, 55, 0.3);">
                    <h2 style="text-align: center; color: #D4AF37; margin-bottom: 5px;">✨ မြန်မာ့ရွှေပန်းတိမ် ✨</h2>
                    <p style="text-align: center; color: #888; font-size: 14px;">အထည်လက်ခံဖြတ်ပိုင်း</p>
                    <hr style="border: 0.5px solid #D4AF37;">
                    <table style="width: 100%; color: white;">
                        <tr><td>အထည်အမည်:</td><td style="text-align: right;"><b>{item_name}</b></td></tr>
                        <tr><td>ရည်မှန်းအလေးချိန်:</td><td style="text-align: right;"><b>{target_w}</b></td></tr>
                        <tr><td>ရည်မှန်းအရှည်:</td><td style="text-align: right;"><b>{target_l}</b></td></tr>
                        <tr><td colspan="2"><br></td></tr>
                        <tr style="color: #D4AF37; font-size: 18px;">
                            <td><b>ပေးရွှေစုစုပေါင်း:</b></td>
                            <td style="text-align: right;"><b>{g_k} ကျပ် {g_p} ပဲ {g_y} ရွေး {g_pt} Pt</b></td>
                        </tr>
                    </table>
                    <br>
                    <p style="font-size: 14px; color: #aaa;">မှတ်ချက်: {note1}</p>
                    <hr style="border: 0.1px solid #444;">
                    <p style="text-align: center; font-size: 12px; color: #D4AF37;">နေ့စွဲ - {now}</p>
                </div>
            """, unsafe_allow_html=True)
            # ၁။ Tab 1 (အထည်ယူ) သိမ်းဆည်းရန်အတွက် ခေတ္တမှတ်သားခြင်း
        st.session_state['take_data'] = {
            "details": f"အထည်ယူ: {item_name} | ဖောက်သည်: {target_l} | မှတ်ချက်: {note1}",
            "weight": f"{g_k} ကျပ် {g_p} ပဲ {g_y} ရွေး {g_pt} Pt"
        }

    with tab2:
        st.subheader("📤 အထည်အပ်နှံခြင်း")
        st.write("💍 **ပြန်အပ်သည့် ရွှေအသား**")
        rk, rp, ry, rpt = st.columns(4)
        ret_k = rk.number_input("ကျပ်", 0, key="ret_k")
        ret_p = rp.number_input("ပဲ", 0, 15, key="ret_p")
        ret_y = ry.number_input("ရွေး", 0, 7, key="ret_y")
        ret_pt = rpt.number_input("Point", 0.0, 9.9, key="ret_pt")
        
        st.write("🔥 **အလျော့တွက်**")
        wk, wp, wy, wpt = st.columns(4)
        was_k = wk.number_input("ကျပ်", 0, key="was_k")
        was_p = wp.number_input("ပဲ", 0, 15, key="was_p")
        was_y = wy.number_input("ရွေး", 0, 7, key="was_y")
        was_pt = wpt.number_input("Point", 0.0, 9.9, key="was_pt")
        
        note2 = st.text_area("မှတ်ချက်", key="note_ret")

        if st.button("ပြေစာထုတ်ရန်"):
            # logic.py ထဲက function ကို ခေါ်ယူနှိုင်းယှဉ်ခြင်း
            diff_res = logic.calculate_gold_difference(g_k, g_p, g_y, g_pt, ret_k, ret_p, ret_y, ret_pt, was_k, was_p, was_y, was_pt)
            now = datetime.now().strftime("%d/%m/%Y %I:%M %p")
            
            # ပိုအပ်လျှင် ရွှေရောင်၊ လိုအပ်လျှင် အနီရောင် ပြပါမည်
            status_color = "#D4AF37" if diff_res['status'] == "ပိုအပ်" else "#FF4B4B"
            
            receipt_html = f"""
            <div style="background-color: #000; border: 4px double #D4AF37; padding: 25px; border-radius: 15px; color: white;">
                <h2 style="text-align: center; color: #D4AF37;">💍 အထည်အပ်နှံမှုပြေစာ</h2>
                <hr style="border: 1px solid #D4AF37;">
                <p>အထည်အမည်: <b>{item_name}</b></p>
                <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                    <tr style="border-bottom: 1px solid #333;">
                        <td style="padding: 10px 0;">ပေးရွှေစုစုပေါင်း</td>
                        <td style="text-align: right;">{g_k}/{g_p}/{g_y}/{g_pt}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #333;">
                        <td style="padding: 10px 0;">ပြန်အပ်ရွှေ (အသား+အလျော့)</td>
                        <td style="text-align: right;">{ret_k+was_k} ကျပ် {(ret_p+was_p)%16} ပဲ ...</td>
                    </tr>
                    <tr>
                        <td style="padding: 20px 0; font-size: 18px; color: {status_color};"><b>{diff_res['status']}ရွှေ</b></td>
                        <td style="text-align: right; font-size: 22px; color: {status_color};">
                            <b>{diff_res['kyat']} ကျပ် {diff_res['pae']} ပဲ {diff_res['yway']} ရွေး {diff_res['point']} Pt</b>
                        </td>
                    </tr>
                </table>
                <p style="text-align: center; margin-top: 25px; font-size: 11px; color: #D4AF37;">✨ {now} ✨</p>
            </div>
            """
            st.markdown(receipt_html, unsafe_allow_html=True)
      
elif menu == "💎 စိန်/ကျောက်/ပုလဲ (အထည်ယူ/အပ်)":
    st.header("💎 စိန်၊ ကျောက်၊ ပုလဲ အထည်ယူ/အပ်")
    
    selected_types = st.multiselect("အသုံးပြုမည့် အမျိုးအစားများ:", ["စိန်", "ကျောက်", "ပုလဲ"])
    
    jewel_data = []
    
    for item in selected_types:
        with st.expander(f"📍 {item} အချက်အလက်များ"):
            col_a, col_b = st.columns(2)
            qty = col_a.number_input(f"{item} အရေအတွက်:", min_value=0, key=f"qty_{item}")
            qual = col_b.text_input(f"{item} အရည်အသွေး:", key=f"qual_{item}")
            
            st.write(f"--- {item} အလေးချိန် ---")
            jk, jp, jy, jpt = st.columns(4)
            k = jk.number_input(f"{item} ကျပ်", key=f"k_{item}")
            p = jp.number_input(f"{item} ပဲ", key=f"p_{item}")
            y = jy.number_input(f"{item} ရွေး", key=f"y_{item}")
            pt = jpt.number_input(f"{item} Pt", key=f"pt_{item}")
            
            jewel_data.append({"type": item, "qty": qty, "qual": qual, "k": k, "p": p, "y": y, "pt": pt})

    st.divider()
    st.subheader("💰 ပေးရွှေချိန်")
    rk, rp, ry, rpt = st.columns(4)
    pk = rk.number_input("ရွှေကျပ်")
    pp = rp.number_input("ရွှေပဲ")
    py = ry.number_input("ရွှေရွေး")
    ppt = rpt.number_input("ရွှေPt")

    # --- ရလဒ်နှင့် ပြေစာထုတ်ရန် ခလုတ် ---
    if st.button("ရလဒ်နှင့် ပြေစာထုတ်ရန်"):
        # ၁။ ပြေစာအတွက် Data တည်ဆောက်ခြင်း
        receipt_data = []
        for d in jewel_data:
            weight_str = format_weight(d['k'], d['p'], d['y'], d['pt'])
            receipt_data.append({
                "အမျိုးအစား": d['type'],
                "အရေအတွက်": d['qty'],
                "အရည်အသွေး": d['qual'],
                "အလေးချိန်": weight_str
            })
        
        gold_str = format_weight(pk, pp, py, ppt)
        receipt_data.append({
            "အမျိုးအစား": "ပေးရွှေ",
            "အရေအတွက်": "-",
            "အရည်အသွေး": "-",
            "အလေးချိန်": gold_str
        })

        # ၂။ စုစုပေါင်းတွက်ချက်ခြင်း
        total_k = pk + sum(d['k'] for d in jewel_data)
        total_p = pp + sum(d['p'] for d in jewel_data)
        total_y = py + sum(d['y'] for d in jewel_data)
        total_pt = ppt + sum(d['pt'] for d in jewel_data)
        final_w = format_weight(total_k, total_p, total_y, total_pt)

        # ၃။ Session State ထဲသို့ ခေတ္တသိမ်းထားခြင်း (Database သိမ်းရန်အတွက်)
        st.session_state['last_receipt'] = receipt_data
        st.session_state['last_total'] = final_w

        # ၄။ ပြေစာကို ဇယားပုံစံဖြင့် ပြသခြင်း
        st.markdown("<h2 style='text-align: center;'>📋 ရွှေနှင့်ကျောက် ပြေစာ</h2>", unsafe_allow_html=True)
        df = pd.DataFrame(receipt_data)
        st.table(df)
        st.success(f"စုစုပေါင်းအလေးချိန်: {final_w}") 
  
elif menu == "💎 3D ဖယောင်းတွက်စက်":
    st.header("💎 3D ဖယောင်းမှ ရွှေချိန်တွက်ချက်ခြင်း")
    
    # Input များ
    wax_w = st.number_input("ဖယောင်းအလေးချိန် (Gram)", value=1.0, step=0.1)
    pae_select = st.selectbox("ပဲရည် ရွေးချယ်ပါ:", [12, 13, 14, 14.2, 15, 15.2, 16])
    
    if st.button("ရွှေချိန်တွက်ရန်"):
        # အခြေခံ ရွှေချိန် (Sprue မပါ)
        res_gold_grams = logic.wax_to_gold_calculator(wax_w, pae_select)
        # Sprue ပါသည့် ရွှေချိန် (၁၅% အပို)
        res_gold_sprue = res_gold_grams * 1.15
        
        # ကျပ်/ပဲ/ရွေး ပြောင်းခြင်း
        k_no, p_no, y_no, pt_no = logic.gram_to_kyat_pae_yway(res_gold_grams)
        k_sp, p_sp, y_sp, pt_sp = logic.gram_to_kyat_pae_yway(res_gold_sprue)
        
        st.markdown(f"""
<div class='kanote-border'>
<h4>📊 ရွှေချိန် ခန့်မှန်းချက်</h4>
<div style="text-align: left;">
<p><b>၁။ အသားတင် ဖယောင်းအလေးချိန်သာ:</b><br>
<span style='color: #888; font-size: 20px;'>{k_no} ကျပ် {p_no} ပဲ {y_no} ရွေး {pt_no} Pt</span></p>
<hr style='border: 0.5px solid #D4AF37;'>
<p><b>၂။ Sprue (ရွှေရည်ဝင်ပေါက်) အပိုထည့်တွက်ပြီး (15%):</b><br>
<span style='color: #D4AF37; font-size: 24px;'><b>{k_sp} ကျပ် {p_sp} ပဲ {y_sp} ရွေး {pt_sp} Pt</b></span></p>
</div>
</div>
""", unsafe_allow_html=True)
        
        st.info("💡 မှတ်ချက် - ဤရလဒ်သည် ပျမ်းမျှတွက်ချက်မှုသာဖြစ်ပါသည်။ မိမိတို့အသုံးပြုနေကျ ဖယောင်းအမျိုးအစားအလိုက် အနည်းငယ် ပြင်ဆင်ရန် လိုအပ်နိုင်ပါသည်။")
   
elif menu == "ကာရက်မှ ရတီဈေးနှုန်းတွက်ချက်ရန်":
    st.title("💎 ကာရက်မှ ရတီဈေးနှုန်းတွက်ချက်ခြင်း")
    
    col1, col2 = st.columns(2)
    with col1:
        carat = st.number_input("ကာရက် (ct) ထည့်ပါ", min_value=0.0, value=5.0)
    with col2:
        price_per_rati = st.number_input("တစ်ရတီဈေးနှုန်း (ကျပ်)", min_value=0, value=15000)
    
    if st.button("တွက်ချက်ရန်"):
        # logic.py ထဲက function ကို ခေါ်သုံးခြင်း
        rati_total, total_price = logic.calculate_rati_price(carat, price_per_rati)
        
        st.markdown("---")
        st.success("### ရလဒ်")
        # Metric ကဒ်လေးတွေနဲ့ ပြသခြင်း
        st.metric(label="စုစုပေါင်း ရတီ (Rati)", value=f"{rati_total:.2f} ရတီ")
        st.metric(label="ကျသင့်ငွေ (ကျပ်)", value=f"{total_price:,.0f} ကျပ်")

elif menu == "ငွေမှ ရွှေတွက်ရန်":
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("🛠️ အချက်အလက်များ")
        cash_input = st.number_input("လက်ရှိငွေသား (ကျပ်)", min_value=0, value=1000000)
        gold_price = st.number_input("၁၆ ပဲရည်ဈေး", min_value=0, value=10900000)
        paeyay = st.selectbox("ပဲရည်:", [16, 15, 14.2, 14, 13, 12])
        
        # Checkbox များဖြင့် ထည့်ချင်မှ ထည့်နိုင်အောင် စီစဉ်ခြင်း
        use_waste = st.checkbox("အလျော့တွက် ထည့်မည်", value=True)
        wastage_val = st.number_input("အလျော့တွက် (ရွေး)", min_value=0.0, value=1.0) if use_waste else 0
        
        use_labor = st.checkbox("လက်ခ ထည့်မည်", value=True)
        labor_val = st.number_input("လက်ခ (ကျပ်)", min_value=0, value=30000) if use_labor else 0
        
        calc_btn = st.button("တွက်ချက်မည်", use_container_width=True)

    with col2:
        st.subheader("💵 ငွေမှ ရွှေ ရလဒ်")
        if calc_btn:
            k, p, y, pt = logic.cash_to_gold_flexible(cash_input, gold_price, wastage_val, labor_val, paeyay, use_waste, use_labor)
            
            # ရလဒ်ကို ကျပ်-ပဲ-ရွေး-ပွိုင့် အစဉ်အတိုင်း စနစ်တကျပြသခြင်း
            st.markdown("""
                <style>
                    .result-box { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6; }
                </style>
            """, unsafe_allow_html=True)
            
            with st.container():
                st.write("---")
                cols = st.columns(4)
                cols[0].metric("ကျပ်", k)
                cols[1].metric("ပဲ", p)
                cols[2].metric("ရွေး", y)
                cols[3].metric("ပွိုင့်", pt)
                st.write("---")
                st.success(f"ရလဒ်: {k} ကျပ် {p} ပဲ {y} ရွေး {pt} ပွိုင့်")
