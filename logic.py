# logic.py
from utils import calculate_pe, format_gold_weight, format_length_inches

# --- ၁။ ရွှေ နှင့် ငွေ Logic ---
def gold_to_money(k, p, y, pt, wk, wp, wy, wpt, gold_price, purity):
    total_p = calculate_pe(k, p, y, pt) + calculate_pe(wk, wp, wy, wpt)
    return (gold_price / 16) * (purity / 16) * total_p

def money_to_gold(budget, gold_price, purity, nk, np, ny, npt):
    one_pe_price = (gold_price / 16) * (purity / 16)
    total_pe_from_money = budget / one_pe_price if one_pe_price > 0 else 0
    wastage_pe = calculate_pe(nk, np, ny, npt)
    return max(0, total_pe_from_money - wastage_pe)

# --- ၂။ အချိုးအစားနှင့် အလေးချိန် Logic ---
def gold_addition(k1, p1, y1, pt1, k2, p2, y2, pt2):
    # စုစုပေါင်း Point တွက်ချက်ခြင်း
    total_pt = (k1*1200 + p1*75 + y1*10 + pt1) + (k2*1200 + p2*75 + y2*10 + pt2)
    return {"kyat": total_pt//1200, "pae": (total_pt%1200)//75, "yway": (total_pt%75)//10, "point": total_pt%10}

def gold_subtraction(k1, p1, y1, pt1, k2, p2, y2, pt2):
    total_pt1 = (k1 * 1200) + (p1 * 75) + (y1 * 10) + pt1
    total_pt2 = (k2 * 1200) + (p2 * 75) + (y2 * 10) + pt2
    diff = total_pt1 - total_pt2
    if diff < 0: return None
    return {"kyat": diff//1200, "pae": (diff%1200)//75, "yway": (diff%75)//10, "point": diff%10}

def weight_per_inch(inch_in, y_per_in, pt_per_in):
    one_inch_pe = (y_per_in / 8) + (pt_per_in / 80)
    return inch_in * one_inch_pe

def length_multiplier_ali(in_m, pe_m, times):
    return (in_m + (pe_m/16)) * times

# --- ၃။ လက်စွပ် နှင့် လက်ကောက် ---
def get_ring_details(r_no):
    # Diameter တွက်ချက်မှု (Formula)
    diameter_mm = 14.01 + (r_no - 4) * 0.5 
    total_inch = (diameter_mm * 3.14159) / 25.4
    return {'mm': round(diameter_mm, 2), 'inch': int(total_inch), 'pe': round((total_inch - int(total_inch)) * 16)}

def bangle_diameter_to_length(inch, pe):
    total_inch = inch + (pe / 16)
    circ_inch = (total_inch * 25.4 * 3.14159) / 25.4
    return int(circ_inch), round((circ_inch - int(circ_inch)) * 16)

# --- ၄။ စိန်၊ ကျောက် နှင့် ရွှေတွက်ချက်မှု ---
def gem_to_gold_units(carat):
    total_gold_points = float(carat) * 19.264
    return {
        "kyat": int(total_gold_points // 120),
        "pae": int((total_gold_points % 120) // 7.5),
        "yway": int((total_gold_points % 7.5) // 1),
        "point": round((total_gold_points % 1) * 10, 1),
        "ratti": round(float(carat) * 1.1, 2)
    }

def calculate_gold_price_comprehensive(kyat, pae, yway, point, gold_price):
    total_pae = (kyat * 16) + pae + (yway / 8) + (point / 80)
    return (total_pae / 16) * gold_price

def calculate_ratio_multiplication(target_inch, ratio_val):
    """
    target_inch: ၂၀ လက်မ
    ratio_val: ၇ (၁ လက်မလျှင် ၇ လက်မနှုန်း)
    """
    total_inches = target_inch * ratio_val
    
    feet = int(total_inches // 12)
    inches = int(total_inches % 12)
    
    return {
        "total_in": total_inches,
        "feet": feet,
        "inches": inches
    }

def weight_per_inch_comprehensive(inch_in, y_per_in, pt_per_in):
    """လက်မအလိုက် ရွှေအလေးချိန်ကို ကျပ်၊ ပဲ၊ ရွေး၊ Point ဖြင့် တွက်ခြင်း"""
    # ၁ လက်မစာ အလေးချိန်ကို Point ဖွဲ့ခြင်း (၁ ရွေး = ၁၀ point)
    one_inch_pts = (y_per_in * 10) + pt_per_in
    
    # စုစုပေါင်း Point = လက်မ အရေအတွက် * ၁ လက်မစာ point
    total_pts = inch_in * one_inch_pts
    
    # Point မှ ကျပ်၊ ပဲ၊ ရွေး ပြန်ခွဲခြင်း
    # ၁ ကျပ် = ၁၂၀၀ pt, ၁ ပဲ = ၇၅ pt, ၁ ရွေး = ၁၀ pt
    kyat = int(total_pts // 1200)
    pae = int((total_pts % 1200) // 75)
    yway = int((total_pts % 75) // 10)
    point = round(total_pts % 10, 1)
    
    return {
        "kyat": kyat,
        "pae": pae,
        "yway": yway,
        "point": point,
        "total_pts": round(total_pts, 2)
    }

def calculate_gold_difference(given_k, given_p, given_y, given_pt, return_k, return_p, return_y, return_pt, waste_k, waste_p, waste_y, waste_pt):
    # အကုန်လုံးကို Point ဖွဲ့ (၁ ကျပ် = ၁၂၀၀, ၁ ပဲ = ၇၅, ၁ ရွေး = ၁၀)
    given_total = (given_k * 1200) + (given_p * 75) + (given_y * 10) + given_pt
    
    # ပြန်အပ်ရွှေ = အထည်အသား + အလျော့တွက်
    return_total = (return_k * 1200) + (return_p * 75) + (return_y * 10) + return_pt
    waste_total = (waste_k * 1200) + (waste_p * 75) + (waste_y * 10) + waste_pt
    actual_return = return_total + waste_total
    
    diff = actual_return - given_total
    
    abs_diff = abs(diff)
    res = {
        "kyat": int(abs_diff // 1200),
        "pae": int((abs_diff % 1200) // 75),
        "yway": int((abs_diff % 75) // 10),
        "point": round(abs_diff % 10, 1),
        "status": "ပိုအပ်" if diff > 0 else "လိုအပ်" if diff < 0 else "ကိုက်ညီ"
    }
    return res

def calculate_gold_difference(given_k, given_p, given_y, given_pt, return_k, return_p, return_y, return_pt, waste_k, waste_p, waste_y, waste_pt):
    # အကုန်လုံးကို Point ဖွဲ့ (၁ ကျပ် = ၁၂၀၀, ၁ ပဲ = ၇၅, ၁ ရွေး = ၁၀)
    given_total = (given_k * 1200) + (given_p * 75) + (given_y * 10) + given_pt
    
    # ပြန်အပ်ရွှေ = အထည်အသား + အလျော့တွက်
    return_total = (return_k * 1200) + (return_p * 75) + (return_y * 10) + return_pt
    waste_total = (waste_k * 1200) + (waste_p * 75) + (waste_y * 10) + waste_pt
    actual_return = return_total + waste_total
    
    diff = actual_return - given_total
    
    abs_diff = abs(diff)
    res = {
        "kyat": int(abs_diff // 1200),
        "pae": int((abs_diff % 1200) // 75),
        "yway": int((abs_diff % 75) // 10),
        "point": round(abs_diff % 10, 1),
        "status": "ပိုအပ်" if diff > 0 else "လိုအပ်" if diff < 0 else "ကိုက်ညီ"
    }
    return res

def wax_to_gold_calculator(wax_weight, pae_ye):
    # ပဲရည်အလိုက် Factor နှုန်းထား (အကြမ်းဖျင်း)
    factors = {
        12: 13.5,
        13: 14.0,
        14: 14.5,
        14.2: 14.6,
        15: 15.0,
        15.2: 15.2,
        16: 15.8
    }
    # ရွေးထားတဲ့ပဲရည်မရှိရင် အလယ်အလတ် 14.5 ကို ယူမယ်
    factor = factors.get(pae_ye, 14.5)
    
    # ရွှေအလေးချိန် = ဖယောင်း * Factor + 15% (Sprue အတွက် အပိုထည့်တွက်ချက်)
    gold_weight = wax_weight * factor * 1.15
    return round(gold_weight, 2)

# 3D ဖယောင်းတွက်စက်အတွက် Logic
def wax_to_gold_calculator(wax_weight, pae_ye):
    # ပဲရည်အလိုက် Factor နှုန်းထားများ
    factors = {
        12: 13.5, 13: 14.0, 14: 14.5, 14.2: 14.6, 
        15: 15.0, 15.2: 15.2, 16: 15.8
    }
    factor = factors.get(pae_ye, 14.5)
    return wax_weight * factor

def gram_to_kyat_pae_yway(grams):
    # ၁ ကျပ် = ၁၆.၆ ဂရမ် (မြန်မာ့ရွှေချိန်စနစ်)
    total_pts = (grams / 16.6) * 1200
    kyat = int(total_pts // 1200)
    pae = int((total_pts % 1200) // 75)
    yway = int((total_pts % 75) // 10)
    point = round(total_pts % 10, 1)
    return kyat, pae, yway, point
# logic.py ဖိုင်ထဲတွင်
def convert_old_system(grams):
    # ၁ ကျပ်သား = ၁၆.၆၀၆ ဂရမ်
    total_kyat = grams / 16.606
    kyat = int(total_kyat)
    pae = int((total_kyat - kyat) * 16)
    yway = round(((total_kyat - kyat) * 16 - pae) * 8)
    return f"{kyat} ကျပ်၊ {pae} ပဲ၊ {yway} ရွေး"

def convert_new_system(grams):
    # ၁ ကျပ်သား = ၁၆.၃၂၉ ဂရမ်
    total_kyat = grams / 16.329
    kyat = int(total_kyat)
    pae = int((total_kyat - kyat) * 16)
    yway = round(((total_kyat - kyat) * 16 - pae) * 8)
    return f"{kyat} ကျပ်၊ {pae} ပဲ၊ {yway} ရွေး"
