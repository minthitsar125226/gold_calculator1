import streamlit as st
from utils import format_gold_weight, calculate_pe

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
    base_unit = st.number_input("အချိုး:", value=7.0)
    multiplier = st.number_input("အရှည်:", value=20.0)
    st.write(f"စုစုပေါင်း: {base_unit * multiplier:.1f}")

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
