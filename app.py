import streamlit as st
from datetime import datetime
from utils import format_gold_weight, calculate_pe, format_length_inches, to_pe
import logic

st.set_page_config(page_title="မြန်မာ့ရွှေပန်းတိမ်သုံး", page_icon="⚒️", layout="wide")

# Theme CSS
st.markdown("<style>.stApp { background-color: #000; color: #fff; } .result-card { background-color: #1a1a1a; padding: 20px; border: 2px solid #D4AF37; border-radius: 12px; color: #D4AF37; text-align: center; margin: 10px 0; }</style>", unsafe_allow_html=True)

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
    st.header("💍 လက်ဝတ်ရတနာ တိုင်းတာခြင်း")
    sub = st.radio("အမျိုးအစား:", ["လက်စွပ် (Ring)", "လက်ကောက် (Bangle)", "ယူနစ် ပြောင်းလဲခြင်း"])
    if sub == "ယူနစ် ပြောင်းလဲခြင်း":
        in_v = st.number_input("လက်မ:", value=20.0)
        p_v = st.selectbox("ပဲ:", list(range(16)))
        st.markdown(f"<div class='result-card'><h2>{format_length_inches(in_v + (p_v/16))}</h2></div>", unsafe_allow_html=True)
    elif sub == "လက်စွပ် (Ring)":
        r_no = st.number_input("Ring Size:", value=15)
        mm = logic.ring_no_to_mm(r_no)
        i, p = logic.mm_to_inch_pe(mm)
        st.markdown(f"<div class='result-card'><h2>{mm:.2f} mm</h2><h3>{i} လက်မ {p} ပဲ</h3></div>", unsafe_allow_html=True)
    elif sub == "လက်ကောက် (Bangle)":
        b_size = st.number_input("လက်တိုင်း (ဥပမာ ၂.၄):", value=2.4)
        st.markdown(f"<div class='result-card'><h2>အလျား: {b_size*25.4*3.14159:.2f} mm</h2></div>", unsafe_allow_html=True)

elif menu == "📋 အထည်ယူ/အထည်အပ်":
    st.header("📋 အထည်ယူ/အပ် နှိုင်းယှဉ်ချက်")
    col_a, col_b = st.columns(2)
    name = col_a.text_input("အမျိုးအမည်:")
    g_pe = calculate_pe(col_a.number_input("ကျပ်(ယူ)",0), col_a.number_input("ပဲ(ယူ)",0), col_a.number_input("ရွေး(ယူ)",0), col_a.number_input("Pt(ယူ)",0))
    r_pe = calculate_pe(col_b.number_input("ကျပ်(အပ်)",0), col_b.number_input("ပဲ(အပ်)",0), col_b.number_input("ရွေး(အပ်)",0), col_b.number_input("Pt(အပ်)",0))
    w_pe = calculate_pe(col_b.number_input("ကျပ်(လျော့)",0), col_b.number_input("ပဲ(လျော့)",0), col_b.number_input("ရွေး(လျော့)",0), col_b.number_input("Pt(လျော့)",0))
    diff = logic.job_comparison(g_pe, r_pe, w_pe)
    st.markdown(f"<div class='result-card'><h2>{'ကျန်:' if diff > 0 else 'ပို:'} {format_gold_weight(abs(diff))}</h2></div>", unsafe_allow_html=True)
