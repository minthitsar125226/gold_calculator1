 import streamlit as st
from datetime import datetime
from utils import format_gold_weight, calculate_pe, format_length_inches, to_pe
import logic

st.set_page_config(page_title="မြန်မာ့ရွှေပန်းတိမ်သုံး", page_icon="⚒️", layout="wide")

# app.py အတွက် CSS
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #D4AF37; }
    h1, h2, h3 { color: #D4AF37 !important; }
    .kanote-border {
        border: 3px double #D4AF37;
        padding: 20px;
        border-radius: 15px;
        background-color: #0a0a0a;
        margin: 20px 0;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
menu = st.sidebar.radio("လုပ်ဆောင်ချက်:", ["🏠 ပင်မ စာမျက်နှာ", "💰 ရွှေ နှင့် ငွေ", "📐 အချိုးအစားတွက်စက်", "💍 လက်စွပ်/လက်ကောက်", "📋 အထည်ယူ/အထည်အပ်", "💎 စိန်/ကျောက်/ပုလဲ"])

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
        st.markdown(f"<div class='kanote-border'><h3>ကျသင့်ငွေ: {int(cost):,} ကျပ်</h3></div>", unsafe_allow_html=True)
    with col2:
        st.subheader("💵 ငွေမှ ရွှေ")
        budget = st.number_input("ရှိသောငွေ:", value=1000000)
        st.write("နုတ်မည့် အလျော့တွက်")
        nk, np, ny, npt = st.columns(4)
        ank, anp, any, anpt = nk.number_input("ကျပ်",0,key="ank"), np.number_input("ပဲ",0,key="anp"), ny.number_input("ရွေး",0,key="any"), npt.number_input("Pt",0,key="anpt")
        pur2 = st.selectbox("ပဲရည်:", [16, 15, 14.2, 14, 13], key="p2")
        if st.button("ငွေမှရွှေ တွက်ရန်"):
            res_g = logic.money_to_gold(budget, gold_price, pur2, ank, anp, any, anpt)
            st.write(f"ရလဒ်: {res_g}")

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
    i_val = ca.number_input("အရှည်(လက်မ)", value=20.0, key="inch_in")
    y_val = cb.number_input("၁လက်မစာရွေး", 0, key="yway_in")
    pt_val = cc.number_input("၁လက်မစာPt", 1, key="pt_in")
    
    if st.button("လက်မအလိုက် တွက်ရန်"):
        res_pe = logic.weight_per_inch(i_val, y_val, pt_val)
        st.write(f"ရလဒ်: {res_pe}")

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
    mode = st.radio("ဘာကို တိုင်းတာချင်ပါသလဲ?", ["လက်စွပ် (Ring)", "လက်ကောက် (Bangle)"])
    
    if mode == "လက်စွပ် (Ring)":
        r_no = st.slider("လက်တိုင်း နံပါတ်ရွေးပါ:", 1, 32, 4)
        details = logic.get_ring_details(r_no)
        st.markdown(f"<div class='kanote-border'><h3>လက်တိုင်း နံပါတ်: {r_no}</h3><p>Diameter: {details['mm']} mm</p><p>အလျား: {details['inch']} လက်မ {details['pe']} ပဲ</p></div>", unsafe_allow_html=True)
        
    elif mode == "လက်ကောက် (Bangle)":
        b_inch = st.number_input("အချင်း (လက်မ):", min_value=1, value=2)
        b_pe = st.number_input("အချင်း (ပဲ):", min_value=0, max_value=15, value=0)
        c_inch, c_pe = logic.bangle_diameter_to_length(b_inch, b_pe)
        st.markdown(f"<div class='kanote-border'><h3>လက်ကောက် အလျား</h3><p>အချင်း: {b_inch} လက်မ {b_pe} ပဲ</p><p><b>ပတ်လည်အလျား: {c_inch} လက်မ {c_pe} ပဲ</b></p></div>", unsafe_allow_html=True)

elif menu == "💎 စိန်/ကျောက်/ပုလဲ":
    st.subheader("💎 စိန်၊ ကျောက်မျက် နှင့် ရွှေထည် တွက်ချက်မှု")
    col1, col2 = st.columns(2)
    with col1:
        gem_type = st.selectbox("အမျိုးအစား:", ["စိန် (Diamond)", "ကျောက်မျက် (Gemstone)", "ပုလဲ (Pearl)"])
        user_carat = st.number_input("ကျောက်အလေးချိန် (Carat):", min_value=0.0, step=0.01, format="%.2f")
        price_per_carat = st.number_input(f"တစ် {gem_type} (1 Carat) ဈေးနှုန်း:", min_value=0, step=10000)
        g_kyat, g_pae, g_yway, g_point = st.number_input("ရွှေ (ကျပ်):", 0), st.number_input("ရွှေ (ပဲ):", 0, 15), st.number_input("ရွှေ (ရွေး):", 0, 7), st.number_input("ရွှေ (Point):", 0.0, 9.9, step=0.1)
        gold_price_val = st.number_input("ယနေ့ ရွှေဈေး (ကျပ်):", value=10000000)

    res = logic.gem_to_gold_units(user_carat)
    gem_cost = user_carat * price_per_carat
    gold_cost = logic.calculate_gold_price_comprehensive(g_kyat, g_pae, g_yway, g_point, gold_price_val)
    total_sum = gem_cost + gold_cost
    with col2:
        st.success("📊 တွက်ချက်မှုရလဒ်")
        st.markdown(f"ကျောက်ဖိုး: **{gem_cost:,.0f} ကျပ်** | ရွှေဖိုး: **{gold_cost:,.0f} ကျပ်**")
        st.markdown(f"<div class='kanote-border'><h2>စုစုပေါင်း</h2><h1>{total_sum:,.0f} ကျပ်</h1></div>", unsafe_allow_html=True)

st.markdown("<hr><p style='text-align: center;'>App by MinThitSarAung</p>", unsafe_allow_html=True)
