import streamlit as st
# utils.py ထဲက Function တွေကို အခုလို Import လုပ်ပေးရပါမယ်
from utils import format_gold_weight, to_pe, from_pe

# ကျန်တဲ့ code တွေ...
st.set_page_config(page_title="မြန်မာ့ရွှေပန်းတိမ်သုံး", page_icon="⚒️", layout="centered")

# Session State စတင်ခြင်း
if 'gold_price' not in st.session_state:
    st.session_state.gold_price = 10900000

st.markdown("<h1 style='text-align: center; color: #D4AF37;'>✨ မြန်မာ့ရွှေပန်းတိမ်သုံး</h1>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["💰 ရွှေ နှင့် ငွေ", "📏 အချိုးအစားတွက်စက်", "🌍 ကမ္ဘာ့ရွှေဈေး", "💍 လက်စွပ်တိုင်း"])

with tab1:
    st.subheader("💰 ရွှေ နှင့် ငွေ လဲလှယ်ခြင်း")
    st.session_state.gold_price = st.number_input("ယနေ့ အခေါက်ရွှေပေါက်ဈေး (ကျပ်):", value=st.session_state.gold_price, step=10000)
    
    sub1, sub2 = st.tabs(["ရွှေမှ ငွေတွက်ရန်", "ငွေမှ ရွှေတွက်ရန်"])
    
    with sub1:
        c1, c2, c3, c4 = st.columns(4)
        k1 = c1.number_input("ကျပ်", value=0, key="k1")
        p1 = c2.number_input("ပဲ", value=0, key="p1")
        y1 = c3.number_input("ရွေး", value=0, key="y1")
        pt1 = c4.number_input("Point", value=0, key="pt1")
        purity = st.selectbox("ရွှေအရည်အသွေး (ပဲရည်):", [16, 15, 14.2, 14, 13], index=0)
        
        total_pe_val = calculate_pe(k1, p1, y1, pt1)
        total_cost = (st.session_state.gold_price / 16) * (purity / 16) * total_pe_val
        st.success(f"စုစုပေါင်းကျသင့်ငွေ: {int(total_cost):,} ကျပ်")

    with sub2:
        budget = st.number_input("ရှိသောငွေ (ကျပ်):", value=1000000, step=10000)
        purity2 = st.selectbox("ဝယ်ယူမည့် ပဲရည်:", [16, 15, 14.2, 14, 13], index=0, key="pur2")
        one_pe_price = (st.session_state.gold_price / 16) * (purity2 / 16)
        total_pe_possible = budget / one_pe_price if one_pe_price > 0 else 0
        st.info(f"ရရှိမည့်ရွှေအသား: {format_gold_weight(total_pe_possible)}")

with tab2:
    st.subheader("📏 ပန်းတိမ်သုံး အလျားနှင့် အလေးချိန်")
    
    # ၁။ အလျားမြှောက်ခြင်း
    st.markdown("#### ၁။ အလျားမြှောက်ခြင်း")
    col_a, col_b = st.columns(2)
    base_unit = col_a.number_input("အချိုး (ဥပမာ- ၇):", value=7.0)
    multiplier = col_b.number_input("မြှောက်မည့် အရှည် (ဥပမာ- ၂၀):", value=20.0)
    total_inches = base_unit * multiplier
    ft = int(total_inches // 12)
    rem_in = total_inches % 12
    st.markdown(f"<div class='result-card'><h4>စုစုပေါင်းအရှည်: {ft} ပေ {rem_in:.1f} လက်မ</h4></div>", unsafe_allow_html=True)
    
    st.divider()
    
    # ၂။ လက်မအလိုက် ရွှေအလေးချိန်
    st.markdown("#### ၂။ လက်မအလိုက် ရွှေအလေးချိန်")
    col_c, col_d, col_e = st.columns(3)
    inch_in = col_c.number_input("အရှည် (လက်မ):", value=20.0, key="inch_in")
    y_per_in = col_d.number_input("၁ လက်မစာ ရွေး:", value=0, key="y_per_in")
    pt_per_in = col_e.number_input("၁ လက်မစာ Point:", value=1, key="pt_per_in")
    total_pe_inch = inch_in * ((y_per_in / 8) + (pt_per_in / 80))
    st.markdown(f"<div class='result-card'><h4>ရလဒ် အလေးချိန်: <br>{format_gold_weight(total_pe_inch)}</h4></div>", unsafe_allow_html=True)
    
    st.divider()
    
    # ၃။ ရွှေအလေးချိန် ပေါင်း/နုတ် တွက်ချက်ခြင်း (အသစ်ထည့်လိုက်သည့် Logic)
    st.markdown("#### ⚖️ ရွှေအလေးချိန် ပေါင်း/နုတ် တွက်ချက်ရန်")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("ပထမအလေးချိန်")
        k1 = st.number_input("ကျပ်", 0, key="k1_add")
        p1 = st.number_input("ပဲ", 0, 15, key="p1_add")
        y1 = st.number_input("ရွေး", 0, 7, key="y1_add")
        pt1 = st.number_input("Point", 0, 9, key="pt1_add")
    
    with col2:
        st.write("ဒုတိယအလေးချိန်")
        k2 = st.number_input("ကျပ်", 0, key="k2_add")
        p2 = st.number_input("ပဲ", 0, 15, key="p2_add")
        y2 = st.number_input("ရွေး", 0, 7, key="y2_add")
        pt2 = st.number_input("Point", 0, 9, key="pt2_add")

    # utils.py က to_pe နဲ့ from_pe ကို ခေါ်သုံးခြင်း
    val1 = to_pe(k1, p1, y1, pt1)
    val2 = to_pe(k2, p2, y2, pt2)
    
    res_add = from_pe(val1 + val2)
    res_sub = from_pe(max(0, val1 - val2))
    
    st.success(f"ပေါင်းလဒ်: {res_add[0]} ကျပ် {res_add[1]} ပဲ {res_add[2]} ရွေး {res_add[3]} Point")
    st.info(f"နုတ်လဒ်: {res_sub[0]} ကျပ် {res_sub[1]} ပဲ {res_sub[2]} ရွေး {res_sub[3]} Point")

with tab3:
    st.subheader("🌍 World Gold to Myanmar")
    w_price = st.number_input("Spot Gold (USD):", value=2100.0)
    u_rate = st.number_input("Dollar Rate (MMK):", value=4800)
    mm_gold = (w_price * u_rate) / 1.875
    st.metric("မြန်မာ့အခေါက်ရွှေဈေး (ခန့်မှန်း)", f"{int(mm_gold):,} ကျပ်")

with tab4:
    st.subheader("💍 လက်စွပ် နှင့် လက်ကောက် တိုင်းတာခြင်း")
    choice = st.radio("ဘာကို တိုင်းတာမှာလဲ:", ["လက်စွပ် (Ring)", "လက်ကောက် (Bangle)"], horizontal=True)
    if choice == "လက်စွပ် (Ring)":
        r_inch = st.selectbox("လက်မ:", [1, 2], index=0)
        r_pe = st.selectbox("ပဲ:", list(range(16)), index=12)
        total = r_inch + (r_pe / 16)
        st.write(f"လုံးပတ်: {total:.2f} လက်မ")
    else:
        b_inch = st.selectbox("လက်မ:", [2, 1], index=0)
        b_pe = st.selectbox("ပဲ:", list(range(16)), index=4)
        total = b_inch + (b_pe / 16)
        st.write(f"အချင်း: {total:.2f} လက်မ")
