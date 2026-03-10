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
    
    # ၁။ အလေးချိန် ပေါင်း/နုတ်
    st.markdown("#### ၁။ ရွှေအလေးချိန် ပေါင်း/နုတ် တွက်ချက်ရန်")
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
    
    c_a, c_s = st.columns(2)
    c_a.success(f"ပေါင်းလဒ်: {format_gold_weight(val1 + val2)}")
    c_s.info(f"နုတ်လဒ်: {format_gold_weight(max(0, val1 - val2))}")

    st.write("---")

    # ၂။ အလျားမြှောက်ခြင်း (မူရင်း Logic)
    st.markdown("#### ၂။ အလျားမြှောက်ခြင်း")
    col_a, col_b = st.columns(2)
    base_unit = col_a.number_input("အချိုး (ဥပမာ- ၇):", value=7.0, key="base_unit")
    multiplier = col_b.number_input("မြှောက်မည့် အရှည် (ဥပမာ- ၂၀):", value=20.0, key="multiplier")
    total_inches = base_unit * multiplier
    ft = int(total_inches // 12)
    rem_in = total_inches % 12
    st.markdown(f"<div class='result-card'><h4>စုစုပေါင်းအရှည်: {ft} ပေ {rem_in:.1f} လက်မ</h4></div>", unsafe_allow_html=True)
    
    st.write("---")
    
    # ၃။ လက်မအလိုက် ရွှေအလေးချိန် (မူရင်း Logic)
    st.markdown("#### ၃။ လက်မအလိုက် ရွှေအလေးချိန်")
    col_c, col_d, col_e = st.columns(3)
    inch_in = col_c.number_input("အရှည် (လက်မ):", value=20.0, key="inch_in")
    y_per_in = col_d.number_input("၁ လက်မစာ ရွေး:", value=0, key="y_per_in")
    pt_per_in = col_e.number_input("၁ လက်မစာ Point:", value=1, key="pt_per_in")
    
    # ၁ လက်မစာ အလေးချိန်ကို ပဲစနစ်ပြောင်း၍ မြှောက်ခြင်း
    one_inch_pe = (y_per_in / 8) + (pt_per_in / 80)
    total_pe_inch = inch_in * one_inch_pe
    st.markdown(f"<div class='result-card'><h4>ရလဒ် အလေးချိန်: <br>{format_gold_weight(total_pe_inch)}</h4></div>", unsafe_allow_html=True)

elif menu == "🌍 ကမ္ဘာ့ရွှေဈေး":
    st.header("🌍 ကမ္ဘာ့ရွှေဈေး တွက်ချက်ခြင်း")
    spot = st.number_input("Spot Gold (USD):", value=2100.0)
    rate = st.number_input("ဒေါ်လာဈေး (မြန်မာကျပ်):", value=4800)
    mm_price = (spot * rate) / 1.875
    st.markdown(f"<div class='result-card'><h2>ခန့်မှန်းအခေါက်ရွှေဈေး: {int(mm_price):,} ကျပ်</h2></div>", unsafe_allow_html=True)

elif menu == "💍 လက်စွပ်/လက်ကောက်":
    st.header("💍 လက်ဝတ်ရတနာ တိုင်းတာခြင်းစနစ်သစ်")
    
    sub_menu = st.radio("အမျိုးအစား ရွေးပါ:", ["လက်စွပ် (Ring)", "လက်ကောက် (Bangle)", "ယူနစ် အပြန်အလှန်ပြောင်းခြင်း"], horizontal=True)

    if sub_menu == "လက်စွပ် (Ring)":
        mode = st.selectbox("တွက်ချက်ပုံ ရွေးပါ:", ["လက်စွပ်နံပါတ်မှ တိုင်းတာချက်သို့", "တိုင်းတာချက်မှ လက်စွပ်နံပါတ်သို့"])
        
        if mode == "လက်စွပ်နံပါတ်မှ တိုင်းတာချက်သို့":
            ring_no = st.number_input("လက်စွပ်နံပါတ် (Ring Size):", value=15, step=1)
            # Standard Ring Size Logic (US Scale approximation)
            mm_val = 11.63 + (ring_no * 0.8128) 
            inch_v, pe_v = mm_to_inch_pe(mm_val)
            st.markdown(f"""<div class='result-card'>
                <h4>လုံးပတ်ရလဒ်</h4>
                <h2>{mm_val:.2f} mm</h2>
                <h3>{inch_v} လက်မ {pe_v} ပဲ</h3>
            </div>""", unsafe_allow_html=True)

        else:
            c1, c2 = st.columns(2)
            in_v = c1.selectbox("လက်မ:", [1, 2], index=1)
            p_v = c2.selectbox("ပဲ:", list(range(16)), index=4)
            mm_res = inch_pe_to_mm(in_v, p_v)
            # Ring No Calculation based on your original logic
            if in_v == 1: r_no = p_v - 8
            else: r_no = p_v + 8
            st.markdown(f"""<div class='result-card'>
                <h4>လက်စွပ်နံပါတ်ရလဒ်</h4>
                <h1 style='font-size: 50px;'>No. {max(1, r_no)}</h1>
                <p>မီလီမီတာ: {mm_res:.2f} mm</p>
            </div>""", unsafe_allow_html=True)

    elif sub_menu == "လက်ကောက် (Bangle)":
        b_mode = st.selectbox("ရွေးချယ်ပါ:", ["အချင်းသိ၍ လက်တိုင်း/အလျားတွက်ရန်", "လက်တိုင်းနံပါတ်သိ၍ အလျားတွက်ရန်"])
        
        if b_mode == "အချင်းသိ၍ လက်တိုင်း/အလျားတွက်ရန်":
            c1, c2 = st.columns(2)
            b_in = c1.selectbox("အချင်း လက်မ:", [1, 2], index=1)
            b_pe = c2.selectbox("အချင်း ပဲ:", list(range(16)), index=4)
            
            diameter_mm = inch_pe_to_mm(b_in, b_pe)
            circumference_mm = diameter_mm * 3.14159 # အလျား (ပတ်လည်)
            st.markdown(f"""<div class='result-card'>
                <h4>လက်ကောက် တိုင်းတာချက်</h4>
                <p>အချင်း: {diameter_mm:.2f} mm</p>
                <h2>အလျား (ပတ်လည်): {circumference_mm:.2f} mm</h2>
                <p>လက်တိုင်း (Diameter): {b_in} လက်မ {b_pe} ပဲ</p>
            </div>""", unsafe_allow_html=True)
            
        else:
            b_size = st.number_input("လက်ကောက် လက်တိုင်း (ဥပမာ- ၂.၄, ၂.၆):", value=2.4, step=0.1)
            # လက်တိုင်းနံပါတ်မှ အလျားတွက်ခြင်း (Diameter * Pi)
            b_mm = b_size * 25.4
            b_circum = b_mm * 3.14159
            st.markdown(f"""<div class='result-card'>
                <h4>လိုအပ်မည့် အလျား</h4>
                <h1 style='font-size: 40px;'>{b_circum:.2f} mm</h1>
                <p>အချင်း: {b_mm:.2f} mm</p>
            </div>""", unsafe_allow_html=True)

    elif sub_menu == "ယူနစ် အပြန်အလှန်ပြောင်းခြင်း":
        st.write("#### 📏 မီလီမီတာ မှ လက်မ/ပဲ/ပေ သို့ ပြောင်းခြင်း")
        input_mm = st.number_input("မီလီမီတာ (mm) ထည့်ပါ:", value=50.0)
        
        total_in = input_mm / 25.4
        ft = int(total_in // 12)
        rem_in = int(total_in % 12)
        rem_pe = round((total_in % 1) * 16)
        
        st.markdown(f"""<div class='result-card'>
            <h4>ပြောင်းလဲပြီး ရလဒ်</h4>
            <h3>{ft} ပေ | {rem_in} လက်မ | {rem_pe} ပဲ</h3>
            <p>စုစုပေါင်းလက်မ: {total_in:.2f} in</p>
        </div>""", unsafe_allow_html=True)
# Static Footer
st.markdown("<div class='main-footer'>App by MinThitSarAung</div>", unsafe_allow_html=True)
