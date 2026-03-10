import streamlit as st
from utils import format_gold_weight, calculate_pe, to_pe, from_pe

# Page Config
st.set_page_config(page_title="မြန်မာ့ရွှေပန်းတိမ်သုံး", page_icon="⚒️", layout="wide")

# Custom CSS for Black and Gold Theme
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .result-card { 
        background-color: #1a1a1a; 
        padding: 20px; 
        border-radius: 10px; 
        border: 2px solid #D4AF37; 
        color: #D4AF37; 
        text-align: center;
        margin: 10px 0px;
    }
    footer {visibility: hidden;}
    .main-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: black;
        color: #D4AF37;
        text-align: center;
        padding: 10px;
        border-top: 1px solid #D4AF37;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #D4AF37;'>🛠 မီနူးများ</h2>", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio(
        "လုပ်ဆောင်ချက် ရွေးချယ်ပါ:",
        ["🏠 ပင်မ စာမျက်နှာ", "💰 ရွှေ နှင့် ငွေ", "📏 အချိုးအစားတွက်စက်", "🌍 ကမ္ဘာ့ရွှေဈေး", "💍 လက်စွပ်/လက်ကောက်"],
        index=0
    )
    st.write("---")
    st.markdown("<p style='text-align: center; color: #D4AF37;'>App by MinThitSarAung</p>", unsafe_allow_html=True)

# Logic for Each Page
if menu == "🏠 ပင်မ စာမျက်နှာ":
    st.markdown("<h1 style='text-align: center; color: #D4AF37;'>✨ မြန်မာ့ရွှေပန်းတိမ်သုံး</h1>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("<h3 style='text-align: center;'>ဘယ်ဘက်ခြမ်းရှိ Sidebar မီနူးမှတစ်ဆင့် လိုအပ်သော တွက်ချက်မှုများကို ရွေးချယ်အသုံးပြုနိုင်ပါသည်။</h3>", unsafe_allow_html=True)

elif menu == "💰 ရွှေ နှင့် ငွေ":
    st.header("💰 ရွှေ နှင့် ငွေ လဲလှယ်ခြင်း")
    gold_price = st.number_input("ယနေ့ အခေါက်ရွှေပေါက်ဈေး (ကျပ်):", value=10900000, step=10000)
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### ရွှေမှ ငွေတွက်ရန်")
        c1, c2, c3, c4 = st.columns(4)
        k = c1.number_input("ကျပ်", 0, key="k")
        p = c2.number_input("ပဲ", 0, 15, key="p")
        y = c3.number_input("ရွေး", 0, 7, key="y")
        pt = c4.number_input("Point", 0, 9, key="pt")
        
        st.write("အလျော့တွက်")
        wc1, wc2, wc3, wc4 = st.columns(4)
        wk = wc1.number_input("ကျပ်", 0, key="wk")
        wp = wc2.number_input("ပဲ", 0, 15, key="wp")
        wy = wc3.number_input("ရွေး", 0, 7, key="wy")
        wpt = wc4.number_input("Point", 0, 9, key="wpt")
        
        purity = st.selectbox("ရွှေအရည်အသွေး (ပဲရည်):", [16, 15, 14.2, 14, 13])
        total_pe = calculate_pe(k, p, y, pt) + calculate_pe(wk, wp, wy, wpt)
        cost = (gold_price / 16) * (purity / 16) * total_pe
        st.markdown(f"<div class='result-card'><h3>စုစုပေါင်းကျသင့်ငွေ: {int(cost):,} ကျပ်</h3></div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("### ငွေမှ ရွှေတွက်ရန်")
        budget = st.number_input("ရှိသောငွေ (ကျပ်):", value=1000000)
        purity2 = st.selectbox("ဝယ်ယူမည့် ပဲရည်:", [16, 15, 14.2, 14, 13], key="p2")
        one_pe_price = (gold_price / 16) * (purity2 / 16)
        res_pe = budget / one_pe_price if one_pe_price > 0 else 0
        st.markdown(f"<div class='result-card'><h3>ရရှိမည့်ရွှေအသား: <br>{format_gold_weight(res_pe)}</h3></div>", unsafe_allow_html=True)

elif menu == "📏 အချိုးအစားတွက်စက်":
    st.header("📏 အချိုးအစားနှင့် အလေးချိန်ပေါင်း/နုတ်")
    
    st.markdown("#### ၁။ အလေးချိန် ပေါင်း/နုတ်")
    col1, col2 = st.columns(2)
    with col1:
        st.write("ပထမအလေးချိန်")
        k1, p1, y1, pt1 = st.columns(4)
        v_k1 = k1.number_input("ကျပ်", 0, key="v_k1")
        v_p1 = p1.number_input("ပဲ", 0, 15, key="v_p1")
        v_y1 = y1.number_input("ရွေး", 0, 7, key="v_y1")
        v_pt1 = pt1.number_input("Point", 0, 9, key="v_pt1")
    
    with col2:
        st.write("ဒုတိယအလေးချိန်")
        k2, p2, y2, pt2 = st.columns(4)
        v_k2 = k2.number_input("ကျပ်", 0, key="v_k2")
        v_p2 = p2.number_input("ပဲ", 0, 15, key="v_p2")
        v_y2 = y2.number_input("ရွေး", 0, 7, key="v_y2")
        v_pt2 = pt2.number_input("Point", 0, 9, key="v_pt2")

    val1 = to_pe(v_k1, v_p1, v_y1, v_pt1)
    val2 = to_pe(v_k2, v_p2, v_y2, v_pt2)
    
    res_add = from_pe(val1 + val2)
    res_sub = from_pe(max(0, val1 - val2))
    
    c_a, c_s = st.columns(2)
    c_a.success(f"ပေါင်းလဒ်: {format_gold_weight(val1 + val2)}")
    c_s.info(f"နုတ်လဒ်: {format_gold_weight(max(0, val1 - val2))}")

elif menu == "🌍 ကမ္ဘာ့ရွှေဈေး":
    st.header("🌍 ကမ္ဘာ့ရွှေဈေး တွက်ချက်ခြင်း")
    spot = st.number_input("Spot Gold (USD):", value=2100.0)
    rate = st.number_input("ဒေါ်လာဈေး (မြန်မာကျပ်):", value=4800)
    mm_price = (spot * rate) / 1.875
    st.markdown(f"<div class='result-card'><h2>ခန့်မှန်းအခေါက်ရွှေဈေး: {int(mm_price):,} ကျပ်</h2></div>", unsafe_allow_html=True)

elif menu == "💍 လက်စွပ်/လက်ကောက်":
    st.header("💍 လက်စွပ် နှင့် လက်ကောက် တိုင်းတာခြင်း")
    mode = st.radio("အမျိုးအစား:", ["လက်စွပ် (Ring)", "လက်ကောက် (Bangle)"], horizontal=True)
    inch = st.selectbox("လက်မ:", [1, 2], index=1)
    pe_size = st.selectbox("ပဲ:", list(range(16)), index=4)
    size_total = inch + (pe_size / 16)
    
    if mode == "လက်စွပ် (Ring)":
        r_no = 4 if size_total < 1.75 else 18
        st.markdown(f"<div class='result-card'><h3>လက်စွပ်နံပါတ်: {r_no}</h3><p>လုံးပတ်: {size_total:.2f} လက်မ</p></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='result-card'><h3>အချင်း: {size_total:.2f} လက်မ</h3></div>", unsafe_allow_html=True)

# Static Footer
st.markdown("<div class='main-footer'>App by MinThitSarAung</div>", unsafe_allow_html=True)
