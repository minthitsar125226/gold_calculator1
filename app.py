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

# Sidebar စတင်သည့်နေရာ
with st.sidebar:
    # ၁။ App နာမည်ကို ရွှေရောင်ဖြင့် ထည့်ခြင်း
    st.markdown("""
        <h2 style='text-align: center; color: #D4AF37; font-family: sans-serif;'>
        ✨ မြန်မာ့ရွှေပန်းတိမ်သုံး ✨
        </h2>
    """, unsafe_allow_html=True)
    
    st.markdown("---") # မျဉ်းကြောင်းလေး ခံပေးပါ

    # ၂။ Menu များ (အစ်ကို့ ရှိပြီးသား code အတိုင်း)
    menu = st.radio("လုပ်ဆောင်ချက်:", [
        "🏠 ပင်မ စာမျက်နှာ", 
        "💰 ရွှေ နှင့် ငွေ", 
        "📐 အချိုးအစားတွက်စက်", 
        "💍 လက်စွပ်/လက်ကောက်", 
        "📋 အထည်ယူ/အထည်အပ်", 
        "💎 စိန်/ကျောက်/ပုလဲ", 
        "💎 3D ဖယောင်းတွက်စက်",
        "💎 စိန်/ကျောက်/ပုလဲ (အထည်ယူ/အပ်)"
    ])
    
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
            # ဂရမ်ရလဒ်ကို အရင်ရယူပါ
            res_g = logic.money_to_gold(budget, gold_price, pur2, ank, anp, any, anpt)
            
            # ဂရမ်ရလဒ်ကို ကျပ်/ပဲ/ရွေး/Point ပြောင်းပါ
            k, p, y, pt = logic.gram_to_kyat_pae_yway(res_g)
            
            # ရလဒ်ကို လှပစွာ ပြသပါ
            st.markdown(f"""
            <div style="background-color: #0E1117; padding: 15px; border-radius: 10px; border: 1px solid #D4AF37;">
                <h4 style="color: #D4AF37;">💰 ရလဒ် (ရွှေချိန်):</h4>
                <p style="font-size: 22px;"><b>{k} ကျပ် {p} ပဲ {y} ရွေး {pt} Point</b></p>
                <p style="font-size: 14px; color: #888;">(စုစုပေါင်း: {res_g:.2f} ဂရမ်)</p>
            </div>
            """, unsafe_allow_html=True)

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

elif menu == "💎 စိန်/ကျောက်/ပုလဲ (အထည်ယူ/အပ်)":
    st.header("💎 စိန်၊ ကျောက်၊ ပုလဲ အထည်ယူ/အပ်")
    
    # ၁။ အမျိုးအစား ရွေးချယ်ခြင်း
    selected_types = st.multiselect("အသုံးပြုမည့် အမျိုးအစားများ:", ["စိန်", "ကျောက်", "ပုလဲ"])
    
    jewel_data = []
    
    # အမျိုးအစားအလိုက် အချက်အလက်များ ဖြည့်စွက်ခြင်း
    for item in selected_types:
        with st.expander(f"📍 {item} အချက်အလက်များ"):
            col_a, col_b = st.columns(2)
            qty = col_a.number_input(f"{item} အရေအတွက်:", min_value=0, key=f"qty_{item}")
            qual = col_b.text_input(f"{item} အရည်အသွေး (ဥပမာ- VVS, AAA):", key=f"qual_{item}")
            
            st.write(f"--- {item} အလေးချိန် ---")
            jk, jp, jy, jpt = st.columns(4)
            k = jk.number_input(f"{item} ကျပ်", key=f"k_{item}")
            p = jp.number_input(f"{item} ပဲ", key=f"p_{item}")
            y = jy.number_input(f"{item} ရွေး", key=f"y_{item}")
            pt = jpt.number_input(f"{item} Pt", key=f"pt_{item}")
            
            col_g, col_c, col_r = st.columns(3)
            gram = col_g.number_input(f"{item} ဂရမ်", format="%.2f", key=f"gram_{item}")
            carat = col_c.number_input(f"{item} ကာရက်", format="%.2f", key=f"ct_{item}")
            rati = col_r.number_input(f"{item} ရတီ", format="%.2f", key=f"r_{item}")
            
            jewel_data.append({"type": item, "qty": qty, "qual": qual, "k": k, "p": p, "y": y, "pt": pt, "gram": gram, "carat": carat, "rati": rati})

    st.divider()
    st.subheader("💰 ပေးရွှေချိန် (ရွှေအသားတင်)")
    rk, rp, ry, rpt = st.columns(4)
    pk = rk.number_input("ရွှေကျပ်")
    pp = rp.number_input("ရွှေပဲ")
    py = ry.number_input("ရွှေရွေး")
    ppt = rpt.number_input("ရွှေPt")

    if st.button("ရလဒ်အားလုံး ဖော်ပြရန်"):
        st.markdown("<div style='border: 2px solid #D4AF37; padding: 15px; border-radius: 10px;'>", unsafe_allow_html=True)
        st.subheader("📊 အထည်အနှစ်ချုပ် စာရင်း")
        
        # ကျောက်အလေးချိန်များ စုပေါင်းခြင်း (ရိုးရှင်းအောင် ကျပ်ကို အခြေခံပြီးပြသည်)
        for d in jewel_data:
            st.write(f"🔹 **{d['type']}** ({d['qty']} ခု) | အရည်အသွေး: **{d['qual']}**")
            st.write(f"   အလေးချိန်: {d['k']} ကျပ် {d['p']} ပဲ {d['y']} ရွေး {d['pt']} Pt")
            st.write(f"   (အပိုယူနစ်: {d['gram']}g | {d['carat']}ct | {d['rati']}r)")
            st.write("---")
        
        st.write(f"🔹 **ပေးရွှေချိန်:** {pk} ကျပ် {pp} ပဲ {py} ရွေး {ppt} Pt")
        
        # အကြမ်းဖျင်း ပေါင်းလဒ် (ရွှေ + ကျောက်ချိန်)
        total_k = pk + sum(d['k'] for d in jewel_data)
        total_p = pp + sum(d['p'] for d in jewel_data)
        total_y = py + sum(d['y'] for d in jewel_data)
        total_pt = ppt + sum(d['pt'] for d in jewel_data)
        
        st.markdown(f"<h3 style='color: #D4AF37;'>စုစုပေါင်း: {total_k} ကျပ် {total_p} ပဲ {total_y} ရွေး {total_pt} Pt</h3>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

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

st.markdown("<hr><p style='text-align: center;'>App by MinThitSarAung</p>", unsafe_allow_html=True)
