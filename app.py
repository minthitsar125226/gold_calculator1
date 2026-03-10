import streamlit as st
from utils import format_gold_weight, calculate_pe, to_pe, from_pe, mm_to_inch_pe, inch_pe_to_mm

st.set_page_config(page_title="မြန်မာ့ရွှေပန်းတိမ်သုံး", page_icon="⚒️", layout="wide")

# Theme CSS
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .result-card { background-color: #1a1a1a; padding: 20px; border-radius: 12px; border: 2px solid #D4AF37; color: #D4AF37; text-align: center; margin: 10px 0px; }
    .main-footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: black; color: #D4AF37; text-align: center; padding: 5px; border-top: 1px solid #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #D4AF37;'>⚒️ မီနူးများ</h2>", unsafe_allow_html=True)
    menu = st.radio(
    "လုပ်ဆောင်ချက် ရွေးချယ်ပါ:",
    ["🏠 ပင်မ စာမျက်နှာ", "💰 ရွှေ နှင့် ငွေ", "📏 အချိုးအစားတွက်စက်", "🌍 ကမ္ဘာ့ရွှေဈေး", "💍 လက်စွပ်/လက်ကောက်", "📋 အထည်ယူ/အထည်အပ်"],
    index=0
    )
    st.info("App by MinThitSarAung")

# ၁။ ပင်မစာမျက်နှာ
if menu == "🏠 ပင်မ စာမျက်နှာ":
    st.markdown("<h1 style='text-align: center; color: #D4AF37;'>✨ မြန်မာ့ရွှေပန်းတိမ်သုံး</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Sidebar မှတစ်ဆင့် လုပ်ဆောင်ချက်များကို ရွေးချယ်ပါ။</h3>", unsafe_allow_html=True)

# ၂။ ရွှေ နှင့် ငွေ (ငွေမှရွှေတွက်ချက်ရာတွင် အလျော့တွက် ထည့်သွင်းထားသည်)
elif menu == "💰 ရွှေ နှင့် ငွေ":
    st.header("💰 ရွှေ နှင့် ငွေ လဲလှယ်ခြင်း")
    gold_price = st.number_input("ယနေ့ အခေါက်ရွှေပေါက်ဈေး (ကျပ်):", value=10900000, step=10000)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚖️ ရွှေမှ ငွေတွက်ရန်")
        c1, c2, c3, c4 = st.columns(4)
        k = c1.number_input("ကျပ်",0,key="k")
        p = c2.number_input("ပဲ",0,key="p")
        y = c3.number_input("ရွေး",0,key="y")
        pt = c4.number_input("Point",0,key="pt")
        st.write("အလျော့တွက်")
        wc1, wc2, wc3, wc4 = st.columns(4)
        wk = wc1.number_input("ကျပ်",0,key="wk")
        wp = wc2.number_input("ပဲ",0,key="wp")
        wy = wc3.number_input("ရွေး",0,key="wy")
        wpt = wc4.number_input("Point",0,key="wpt")
        purity = st.selectbox("ပဲရည်:", [16, 15, 14.2, 14, 13])
        total_p = calculate_pe(k, p, y, pt) + calculate_pe(wk, wp, wy, wpt)
        cost = (gold_price / 16) * (purity / 16) * total_p
        st.markdown(f"<div class='result-card'><h3>ကျသင့်ငွေ: {int(cost):,} ကျပ်</h3></div>", unsafe_allow_html=True)

    with col2:
        st.subheader("💵 ငွေမှ ရွှေတွက်ရန်")
        budget = st.number_input("ရှိသောငွေ (ကျပ်):", value=1000000)
        st.write("နုတ်မည့် အလျော့တွက်")
        nc1, nc2, nc3, nc4 = st.columns(4)
        nk = nc1.number_input("ကျပ်",0,key="nk")
        np = nc2.number_input("ပဲ",0,key="np")
        ny = nc3.number_input("ရွေး",0,key="ny")
        npt = nc4.number_input("Point",0,key="npt")
        purity2 = st.selectbox("ဝယ်ယူမည့် ပဲရည်:", [16, 15, 14.2, 14, 13], key="p2")
        
        one_pe_price = (gold_price / 16) * (purity2 / 16)
        total_pe_from_money = budget / one_pe_price if one_pe_price > 0 else 0
        wastage_pe = calculate_pe(nk, np, ny, npt)
        final_gold_pe = max(0, total_pe_from_money - wastage_pe)
        
        st.markdown(f"<div class='result-card'><h3>ရရှိမည့် ရွှေအသား: <br>{format_gold_weight(final_gold_pe)}</h3></div>", unsafe_allow_html=True)

elif menu == "📏 အချိုးအစားတွက်စက်":
    st.header("📏 အချိုးအစားနှင့် အလေးချိန် တွက်ချက်ခြင်း")
    
    # ၁။ အလေးချိန် ပေါင်း/နုတ်
    st.subheader("⚖️ ၁။ ရွှေအလေးချိန် ပေါင်း/နုတ်")
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

    # ၂။ အလျားမြှောက်ခြင်း (ဥပမာ- ကြိုးအရှည်တွက်ခြင်း)
    st.subheader("📏 ၂။ အလျားမြှောက်ခြင်း")
    col_x, col_y = st.columns(2)
    with col_x:
        base_unit = st.number_input("အချိုး (ဥပမာ- ၇):", value=7.0, key="base_unit")
        multiplier = st.number_input("မြှောက်မည့်အရှည် (ဥပမာ- ၂၀):", value=20.0, key="multiplier")
        total_inches = base_unit * multiplier
        ft = int(total_inches // 12)
        rem_in = total_inches % 12
        st.markdown(f"<div class='result-card'><h4>စုစုပေါင်းအရှည်: <br>{ft} ပေ {rem_in:.1f} လက်မ</h4></div>", unsafe_allow_html=True)
    
    with col_y:
        st.write("အလျားရှင်းလင်းချက်")
        st.info(f"စုစုပေါင်း: {total_inches:.1f} လက်မ")

    st.write("---")
    
    # ၃။ လက်မအလိုက် ရွှေအလေးချိန် (Gold weight per inch)
    st.subheader("⚖️ ၃။ လက်မအလိုက် ရွှေအလေးချိန်")
    col_c, col_d, col_e = st.columns(3)
    inch_in = col_c.number_input("အရှည် (လက်မ):", value=20.0, key="inch_in")
    y_per_in = col_d.number_input("၁ လက်မစာ ရွေး:", value=0, key="y_per_in")
    pt_per_in = col_e.number_input("၁ လက်မစာ Point:", value=1, key="pt_per_in")
    
    # ၁ လက်မစာ အလေးချိန်ကို ပဲစနစ်ပြောင်း၍ မြှောက်ခြင်း
    one_inch_pe = (y_per_in / 8) + (pt_per_in / 80)
    total_pe_inch = inch_in * one_inch_pe
    
    st.markdown(f"""
        <div class='result-card'>
            <h4>ရလဒ် အလေးချိန်:</h4>
            <h2>{format_gold_weight(total_pe_inch)}</h2>
            <p>စုစုပေါင်း ပဲယူနစ်: {total_pe_inch:.4f}</p>
        </div>
    """, unsafe_allow_html=True)

# ၅။ လက်စွပ်/လက်ကောက် (ယူနစ်ပြောင်းလဲခြင်းတွင် ပေ တွက်ချက်မှု ထည့်သွင်းထားသည်)
elif menu == "💍 လက်စွပ်/လက်ကောက်":
    st.header("💍 လက်ဝတ်ရတနာ တိုင်းတာခြင်း")
    sub = st.radio("အမျိုးအစား:", ["လက်စွပ် (Ring)", "လက်ကောက် (Bangle)", "ယူနစ် ပြောင်းလဲခြင်း"], horizontal=True)
    
    if sub == "ယူနစ် ပြောင်းလဲခြင်း":
        st.subheader("📏 လက်မ/ပဲ မှ ပေ သို့ တွက်ချက်ခြင်း")
        c1, c2 = st.columns(2)
        in_v = c1.number_input("လက်မ ထည့်ပါ:", value=20.0)
        p_v = c2.selectbox("ပဲ ထည့်ပါ:", list(range(16)), key="up_pe")
        
        total_in = in_v + (p_v / 16)
        ft = int(total_in // 12)
        rem_in = int(total_in % 12)
        rem_pe = round((total_in % 1) * 16)
        
        st.markdown(f"""<div class='result-card'>
            <h4>ပြောင်းလဲပြီး ရလဒ်</h4>
            <h2>{ft} ပေ | {rem_in} လက်မ | {rem_pe} ပဲ</h2>
            <p>စုစုပေါင်း မီလီမီတာ: {total_in * 25.4:.2f} mm</p>
        </div>""", unsafe_allow_html=True)
    
    # (ကျန်သည့် လက်စွပ် နှင့် လက်ကောက် logic များ ယခင်အတိုင်း)
    elif sub == "လက်စွပ် (Ring)":
        m = st.selectbox("တွက်ချက်ပုံ:", ["လက်စွပ်နံပါတ်မှ တိုင်းတာချက်သို့", "တိုင်းတာချက်မှ လက်စွပ်နံပါတ်သို့"])
        if m == "လက်စွပ်နံပါတ်မှ တိုင်းတာချက်သို့":
            r_no = st.number_input("Ring Size:", value=15)
            mm = 11.63 + (r_no * 0.8128)
            i, p = mm_to_inch_pe(mm)
            st.markdown(f"<div class='result-card'><h2>{mm:.2f} mm</h2><h3>{i} လက်မ {p} ပဲ</h3></div>", unsafe_allow_html=True)
        else:
            in_v_r = st.selectbox("လက်မ:", [1,2], index=1, key="in_r")
            p_v_r = st.selectbox("ပဲ:", list(range(16)), index=4, key="p_r")
            mm_res = inch_pe_to_mm(in_v_r, p_v_r)
            r_no = (p_v_r-8) if in_v_r==1 else (p_v_r+8)
            st.markdown(f"<div class='result-card'><h1>No. {max(1, r_no)}</h1><p>{mm_res:.2f} mm</p></div>", unsafe_allow_html=True)
    
    elif sub == "လက်ကောက် (Bangle)":
        bm = st.selectbox("ရွေးချယ်ပါ:", ["အချင်းသိ၍ လက်တိုင်း/အလျားတွက်ရန်", "လက်တိုင်းနံပါတ်သိ၍ အလျားတွက်ရန်"])
        if bm == "အချင်းသိ၍ လက်တိုင်း/အလျားတွက်ရန်":
            c1, c2 = st.columns(2)
            b_in = c1.selectbox("အချင်း (လက်မ):", [1, 2], index=1)
            b_pe = c2.selectbox("အချင်း (ပဲ):", list(range(16)), index=4)
            d_mm = inch_pe_to_mm(b_in, b_pe)
            st.markdown(f"<div class='result-card'><h2>အလျား (ပတ်လည်): {d_mm*3.14159:.2f} mm</h2><p>အချင်း: {d_mm:.2f} mm</p></div>", unsafe_allow_html=True)
        else:
            b_size = st.number_input("လက်ကောက် လက်တိုင်း (ဥပမာ ၂.၄):", value=2.4)
            st.markdown(f"<div class='result-card'><h2>လိုအပ်မည့်အလျား: {b_size*25.4*3.14159:.2f} mm</h2></div>", unsafe_allow_html=True)

elif menu == "📋 အထည်ယူ/အထည်အပ်":
    st.header("📋 အထည်ယူ နှင့် အထည်အပ်နှံခြင်း")
    
    col_order, col_return = st.columns(2)
    
    with col_order:
        st.subheader("📦 ၁။ အထည်ယူ (Job Order)")
        item_name = st.text_input("အမျိုးအမည် (ဥပမာ- နေတိုးကြိုး):", key="item_name")
        target_weight = st.text_input("တင်ရမည့် ရွှေချိန် (ဥပမာ- ၁ ကျပ်):", key="target_w")
        item_length = st.text_input("ကြိုးအရှည် (ဥပမာ- ၁၈ လက်မ):", key="item_len")
        
        st.write("---")
        st.write("📥 **ပေးရွှေ (အသားတင်)**")
        oc1, oc2, oc3, oc4 = st.columns(4)
        ok = oc1.number_input("ကျပ်", 0, key="ok")
        op = oc2.number_input("ပဲ", 0, 15, key="op")
        oy = oc3.number_input("ရွေး", 0, 7, key="oy")
        opt = oc4.number_input("Point", 0, 9, key="opt")
        
        give_gold_total = calculate_pe(ok, op, oy, opt)
        st.markdown(f"<div class='result-card'><h4>စုစုပေါင်း ပေးရွှေ:</h4><h3>{format_gold_weight(give_gold_total)}</h3></div>", unsafe_allow_html=True)

    with col_return:
        st.subheader("📤 ၂။ ပြန်အပ် (Job Return)")
        st.info(f"အမျိုးအမည်: {item_name if item_name else '-'}")
        
        st.write("---")
        st.write("📤 **ပြန်အပ်ရွှေ (အသားတင်)**")
        rc1, rc2, rc3, rc4 = st.columns(4)
        rk = rc1.number_input("ကျပ်", 0, key="rk")
        rp = rc2.number_input("ပဲ", 0, 15, key="rp")
        ry = rc3.number_input("ရွေး", 0, 7, key="ry")
        rpt = rc4.number_input("Point", 0, 9, key="rpt")
        
        st.write("➕ **ရရှိမည့် အလျော့တွက်**")
        wc1, wc2, wc3, wc4 = st.columns(4)
        wk = wc1.number_input("ကျပ်", 0, key="wk")
        wp = wc2.number_input("ပဲ", 0, 15, key="wp")
        wy = wc3.number_input("ရွေး", 0, 7, key="wy")
        wpt = wc4.number_input("Point", 0, 9, key="wpt")
        
        # ပြန်အပ်ရွှေ စုစုပေါင်း = အသားတင် + အလျော့တွက်
        return_net_pe = calculate_pe(rk, rp, ry, rpt)
        wastage_pe = calculate_pe(wk, wp, wy, wpt)
        total_return_with_wastage = return_net_pe + wastage_pe
        
        # ပေးရွှေ နှင့် (ပြန်အပ်ရွှေ + အလျော့တွက်) နှိုင်းယှဉ်ခြင်း
        diff_pe = give_gold_total - total_return_with_wastage
        
        st.write("---")
        st.subheader("⚖️ တွက်ချက်မှုရလဒ်")
        
        if diff_pe > 0:
            st.warning(f"အပ်ရန်ကျန်ရှိနေသေးသည်: \n {format_gold_weight(diff_pe)}")
        elif diff_pe < 0:
            st.success(f"ပိုအပ်ထားသည်: \n {format_gold_weight(abs(diff_pe))}")
        else:
            st.success("အလေးချိန် ကိုက်ညီမှုရှိပါသည်။")

        st.markdown(f"""
            <div class='result-card'>
                <p>ပေးရွှေ: {format_gold_weight(give_gold_total)}</p>
                <p>ပြန်အပ် (အသား + အလျော့): {format_gold_weight(total_return_with_wastage)}</p>
            </div>
        """, unsafe_allow_html=True)
        
# --- ကျစ်လျစ်သော ပြေစာပုံစံ ---
        st.write("---")
        if st.button("📄 ပြေစာထုတ်ရန် (Preview)"):
            # ပြေစာ Size ကို width: 300px ပတ်ချာလည်အထိ ချုံ့ထားပါတယ်
            receipt_html = f"""
            <div id="receipt" style="
                background-color: white; 
                color: black; 
                padding: 15px; 
                border: 3px double #D4AF37; 
                border-radius: 8px; 
                font-family: 'Pyidaungsu', sans-serif; 
                width: 280px; 
                margin: auto;
                line-height: 1.4;
            ">
                <h4 style="text-align: center; color: #D4AF37; margin-bottom: 5px;">အထည်ယူ/အပ် ပြေစာ</h4>
                <p style="font-size: 12px; text-align: center; margin-top: 0;">နေ့စွဲ: {st.date_input("Date", key="d_final").strftime('%d-%m-%Y')}</p>
                <hr style="border: 0.5px solid #eee;">
                <div style="font-size: 13px;">
                    <p><b>အမျိုးအမည်:</b> {item_name if item_name else '-'}</p>
                    <p><b>တင်ရမည့်ချိန်:</b> {target_weight if target_weight else '-'}</p>
                    <p>📥 <b>ပေးရွှေ:</b> {format_gold_weight(give_gold_total)}</p>
                    <p>📤 <b>ပြန်အပ်:</b> {format_gold_weight(return_net_pe)}</p>
                    <p>➕ <b>အလျော့:</b> {format_gold_weight(wastage_pe)}</p>
                </div>
                <hr style="border: 0.5px solid #eee;">
                <div style="text-align: center; background: #f9f9f9; padding: 5px; border-radius: 5px;">
                    <b style="font-size: 14px; color: {'red' if diff_pe > 0 else 'green'};">
                        {'ကျန်ရှိ:' if diff_pe > 0 else 'ပိုအပ်:'} {format_gold_weight(abs(diff_pe))}
                    </b>
                </div>
                <p style="text-align: center; font-size: 10px; color: #888; margin-top: 10px;">App by MinThitSarAung</p>
            </div>
            """
            st.markdown(receipt_html, unsafe_allow_html=True)
            
            # Image သိမ်းရန် လမ်းညွှန်
            st.success("အပေါ်က ပြေစာကတ်လေးကို Screenshot ရိုက်၍ သိမ်းဆည်းနိုင်ပါပြီ။")

st.markdown("<div class='main-footer'>App by MinThitSarAung</div>", unsafe_allow_html=True)
    
