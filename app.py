import streamlit as st
from datetime import datetime
from utils import format_gold_weight, calculate_pe, format_length_inches, to_pe
import logic


st.set_page_config(page_title="မြန်မာ့ရွှေပန်းတိမ်သုံး", page_icon="⚒️", layout="wide")

# app.py အတွက် CSS
st.markdown("""
    <style>
    /* တစ်ခုလုံးအတွက် ရွှေရောင် စာသား */
    .stApp { background-color: #000000; color: #D4AF37; }
    
    /* ရွှေရောင် ခေါင်းစဉ်များ */
    h1, h2, h3 { color: #D4AF37 !important; }

    /* ကနုတ်ဒီဇိုင်း (Border Style) */
    .kanote-border {
        border: 3px double #D4AF37;
        padding: 20px;
        border-radius: 15px;
        background-color: #0a0a0a;
        margin: 20px 0;
        text-align: center;
    }

    /* App by MinThitSarAung အတွက် ကနုတ်ဖောင့်ပုံစံ */
    .footer-kanote {
        position: fixed;
        left: 0; bottom: 0; width: 100%;
        background-color: #000000;
        color: #D4AF37;
        text-align: center;
        padding: 10px;
        border-top: 2px solid #D4AF37;
        font-family: 'Georgia', serif;
        font-style: italic;
        letter-spacing: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
menu = st.sidebar.radio("လုပ်ဆောင်ချက်:", ["🏠 ပင်မ စာမျက်နှာ", "💰 ရွှေ နှင့် ငွေ", "📏 အချိုးအစားတွက်စက်", "💍 လက်စွပ်/လက်ကောက်", "📋 အထည်ယူ/အထည်အပ်"])

if menu == "🏠 ပင်မ စာမျက်နှာ":
    st.markdown("<h1 style='text-align: center; color: #D4AF37;'>✨ မြန်မာ့ရွှေပန်းတိမ်သုံး</h1>", unsafe_allow_html=True)

elif menu == "💰 ရွှေ နှင့် ငွေ":
    st.header("💰 ရွှေ နှင့် ငွေ လဲလှယ်ခြင်း")
    gold_price = st.number_input("အခေါက်ရွှေဈေး:", value=10900000)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⚖️ ရွှေမှ ငွေ")
        k, p, y, pt = st.columns(4)
        gk, gp, gy, gpt = k.number_input("ကျပ်",0,key="gk"), p.number_input("ပဲ",0,key="gp"), y.number_input("ရွေး",0,key="gy"), pt.number_input("Pt",0,key="gpt")
        st.write("အလျော့တွက်")
        wk, wp, wy, wpt = st.columns(4)
        awk, awp, awy, awpt = wk.number_input("ကျပ်",0,key="awk"), wp.number_input("ပဲ",0,key="awp"), wy.number_input("ရွေး",0,key="awy"), wpt.number_input("Pt",0,key="awpt")
        pur = st.selectbox("ပဲရည်:", [16, 15, 14.2, 14, 13], key="p1")
        cost = logic.gold_to_money(gk, gp, gy, gpt, awk, awp, awy, awpt, gold_price, pur)
        st.markdown(f"<div class='result-card'><h3>ကျသင့်ငွေ: {int(cost):,} ကျပ်</h3></div>", unsafe_allow_html=True)
    with col2:
        st.subheader("💵 ငွေမှ ရွှေ")
        budget = st.number_input("ရှိသောငွေ:", value=1000000)
        st.write("နုတ်မည့် အလျော့တွက်")
        nk, np, ny, npt = st.columns(4)
        ank, anp, any, anpt = nk.number_input("ကျပ်",0,key="ank"), np.number_input("ပဲ",0,key="anp"), ny.number_input("ရွေး",0,key="any"), npt.number_input("Pt",0,key="anpt")
        pur2 = st.selectbox("ပဲရည်:", [16, 15, 14.2, 14, 13], key="p2")
        res_g = logic.money_to_gold(budget, gold_price, pur2, ank, anp, any, anpt)
        st.markdown(f"<div class='result-card'><h3>ရွှေအသား: <br>{format_gold_weight(res_g)}</h3></div>", unsafe_allow_html=True)

elif menu == "📏 အချိုးအစားတွက်စက်":
    st.header("📏 အချိုးအစားနှင့် အလေးချိန် တွက်ချက်ခြင်း")
    # ပေါင်း/နုတ်
    st.subheader("⚖️ ၁။ ရွှေအလေးချိန် ပေါင်း/နုတ်")
    c1, c2 = st.columns(2)
    v1 = to_pe(c1.number_input("ကျပ်(1)",0), c1.number_input("ပဲ(1)",0), c1.number_input("ရွေး(1)",0), c1.number_input("Pt(1)",0))
    v2 = to_pe(c2.number_input("ကျပ်(2)",0), c2.number_input("ပဲ(2)",0), c2.number_input("ရွေး(2)",0), c2.number_input("Pt(2)",0))
    st.success(f"ပေါင်းလဒ်: {format_gold_weight(v1+v2)}")
    # လက်မအလိုက်
    st.subheader("⚖️ ၂။ လက်မအလိုက် ရွှေအလေးချိန်")
    ca, cb, cc = st.columns(3)
    res_pe = logic.weight_per_inch(ca.number_input("အရှည်(လက်မ)", value=20.0), cb.number_input("၁လက်မစာရွေး", 0), cc.number_input("၁လက်မစာPt", 1))
    st.markdown(f"<div class='result-card'><h2>{format_gold_weight(res_pe)}</h2></div>", unsafe_allow_html=True)
    # အလီ
    st.subheader("📏 ၃။ အလျားမြှောက်စက် (အလီ)")
    la, lb, lc = st.columns(3)
    total_l = logic.length_multiplier_ali(la.number_input("လက်မ", 6), lb.selectbox("ပဲ", list(range(16))), lc.number_input("အလီ", 3))
    st.markdown(f"<div class='result-card'><h2>{format_length_inches(total_l)}</h2></div>", unsafe_allow_html=True)

elif menu == "💍 လက်စွပ်/လက်ကောက်":
    st.subheader("💍 လက်စွပ် နှင့် လက်ကောက် တိုင်းတာခြင်း")
    
    # mode ကို အရင်သတ်မှတ်ပါ
    mode = st.radio("ဘာကို တိုင်းတာချင်ပါသလဲ?", ["လက်စွပ် (Ring)", "လက်ကောက် (Bangle)"])
    
    # Indentation (အကွာအဝေး) ညီညာစွာ ရေးပါ
    if mode == "လက်စွပ် (Ring)":
        r_no = st.slider("လက်တိုင်း နံပါတ်ရွေးပါ:", 1, 32, 4)
        details = logic.get_ring_details(r_no)
        st.markdown(f"""
            <div class='kanote-border'>
                <h3>လက်တိုင်း နံပါတ်: {r_no}</h3>
                <p>Diameter: {details['mm']} mm</p>
                <p>အလျား: {details['inch']} လက်မ {details['pe']} ပဲ</p>
        
    elif mode == "လက်ကောက် (Bangle)":
        b_inch = st.number_input("အချင်း (လက်မ):", min_value=1, value=2)
        b_pe = st.number_input("အချင်း (ပဲ):", min_value=0, max_value=15, value=0)
        
        # Logic ကို ခေါ်သုံးခြင်း
        c_inch, c_pe = logic.bangle_diameter_to_length(b_inch, b_pe)
        
        st.markdown(f"""
            <div class='kanote-border'>
                <h3>လက်ကောက် အလျား</h3>
                <p>အချင်း: {b_inch} လက်မ {b_pe} ပဲ</p>
                <p><b>ပတ်လည်အလျား: {c_inch} လက်မ {c_pe} ပဲ</b></p>
            </div>""", unsafe_allow_html=True)

elif menu == "📋 အထည်ယူ/အထည်အပ်":
    st.header("📋 အထည်ယူ/အပ် နှိုင်းယှဉ်ချက်")
    col_a, col_b = st.columns(2)
    name = col_a.text_input("အမျိုးအမည်:")
    g_pe = calculate_pe(col_a.number_input("ကျပ်(ယူ)",0), col_a.number_input("ပဲ(ယူ)",0), col_a.number_input("ရွေး(ယူ)",0), col_a.number_input("Pt(ယူ)",0))
    r_pe = calculate_pe(col_b.number_input("ကျပ်(အပ်)",0), col_b.number_input("ပဲ(အပ်)",0), col_b.number_input("ရွေး(အပ်)",0), col_b.number_input("Pt(အပ်)",0))
    w_pe = calculate_pe(col_b.number_input("ကျပ်(လျော့)",0), col_b.number_input("ပဲ(လျော့)",0), col_b.number_input("ရွေး(လျော့)",0), col_b.number_input("Pt(လျော့)",0))
    diff = logic.job_comparison(g_pe, r_pe, w_pe)
    st.markdown(f"<div class='result-card'><h2>{'ကျန်:' if diff > 0 else 'ပို:'} {format_gold_weight(abs(diff))}</h2></div>", unsafe_allow_html=True)
    # အောက်ဆုံးမှာ ဒါလေး ထည့်ပါ
st.markdown("<p style='text-align: center;'>App by MinThitSarAung</p>", unsafe_allow_html=True)
