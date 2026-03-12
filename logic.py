# logic.py
from utils import calculate_pe, format_gold_weight, format_length_inches

# --- ၁။ ရွှေ နှင့် ငွေ Logic ---
def gold_to_money(k, p, y, pt, wk, wp, wy, wpt, gold_price, purity):
    """ရွှေအလေးချိန်မှ ကျသင့်ငွေတွက်ခြင်း (အလျော့တွက်ပေါင်းသည်)"""
    total_p = calculate_pe(k, p, y, pt) + calculate_pe(wk, wp, wy, wpt)
    return (gold_price / 16) * (purity / 16) * total_p

def money_to_gold(budget, gold_price, purity, nk, np, ny, npt):
    """ငွေမှ ရွှေအသားတွက်ခြင်း (အလျော့တွက်နုတ်သည်)"""
    one_pe_price = (gold_price / 16) * (purity / 16)
    total_pe_from_money = budget / one_pe_price if one_pe_price > 0 else 0
    wastage_pe = calculate_pe(nk, np, ny, npt)
    return max(0, total_pe_from_money - wastage_pe)

# --- ၂။ အချိုးအစားနှင့် အလေးချိန် Logic ---
def weight_per_inch(inch_in, y_per_in, pt_per_in):
    """လက်မအလိုက် ရွှေအလေးချိန်တွက်ခြင်း"""
    one_inch_pe = (y_per_in / 8) + (pt_per_in / 80)
    return inch_in * one_inch_pe

def length_multiplier_ali(in_m, pe_m, times):
    """အလျားအလီမြှောက်ခြင်း (အလီ)"""
    return (in_m + (pe_m/16)) * times


# U HTON Chart ဇယားပါ တန်ဖိုးများအားလုံး
RING_SIZE_DATA = {
    1: 13.05, 2: 13.37, 3: 13.69, 4: 14.01, 5: 14.32, 6: 14.64, 
    7: 14.96, 8: 15.28, 9: 15.60, 10: 15.92, 11: 16.23, 12: 16.55,
    13: 16.87, 14: 17.19, 15: 17.56, 16: 17.83, 17: 18.14, 18: 18.46,
    19: 18.78, 20: 19.10, 21: 19.42, 22: 19.74, 23: 20.05, 24: 20.37,
    25: 20.69, 26: 21.01, 27: 21.33, 28: 21.65, 29: 19.96, 30: 22.28,
    31: 22.60, 32: 22.92
}

def mm_to_inch_pe(mm_value):
    """mm မှ လက်မနှင့် ပဲ သို့ပြောင်းရန်"""
    # 1 inch = 25.4 mm
    total_inch = mm_value / 25.4
    inch = int(total_inch)
    # 1 လက်မ = 16 ပဲ
    pe = round((total_inch - inch) * 16)
    return inch, pe

def get_ring_details(ring_no):
    """လက်တိုင်းနံပါတ်မှ အချက်အလက်အပြည့်အစုံထုတ်ပေးရန်"""
    diameter_mm = RING_SIZE_DATA.get(ring_no, 0)
    circumference_mm = diameter_mm * 3.14159
    
    diameter_inch, diameter_pe = mm_to_inch_pe(diameter_mm)
    
    return {
        "mm": diameter_mm,
        "inch": diameter_inch,
        "pe": diameter_pe,
        "circ": circumference_mm
    }

def bangle_diameter_to_length(inch, pe):
    total_inch = inch + (pe / 16)
    circ_mm = (total_inch * 25.4) * 3.14159
    total_inch_res = circ_mm / 25.4
    c_inch = int(total_inch_res)
    c_pe = round((total_inch_res - c_inch) * 16)
    return c_inch, c_pe

# --- ၄။ အထည်ယူ/အပ် Logic ---
def job_comparison(give_total_pe, return_net_pe, wastage_pe):
    """ပေးရွှေ နှင့် (ပြန်အပ် + အလျော့) နှိုင်းယှဉ်ခြင်း"""
    total_return = return_net_pe + wastage_pe
    return give_total_pe - total_return

def get_ring_details(r_no):
    # ၁။ Diameter ရှာခြင်း (ဥပမာ Formula)
    diameter_mm = 14.01 + (r_no - 4) * 0.5 
    # ၂။ ပတ်လည်အလျား (Circumference) ကို mm နဲ့ အရင်ရှာ
    length_mm = diameter_mm * 3.14159
    
    # ၃။ mm ကို လက်မ အပြည့်အစုံပြောင်း (25.4 နဲ့ စား)
    total_inch = length_mm / 25.4  
    
    # ၄။ လက်မ နှင့် ပဲ ခွဲထုတ်ခြင်း
    inch = int(total_inch) # လက်မ အပြည့် (ဥပမာ - 0 သို့မဟုတ် 1)
    # ကျန်တဲ့ ဓာတ်သမကို ၁၆ နဲ့မြှောက်ပြီး "ပဲ" ရှာခြင်း
    pe = round((total_inch - inch) * 16) 
    
    return {'mm': round(diameter_mm, 2), 'inch': inch, 'pe': pe}

def gem_to_gold_units(carat):
    ratti = float(carat) * 1.1
    total_gold_points = float(carat) * 19.264
    
    kyat = int(total_gold_points // 120)
    pae = int((total_gold_points % 120) // 7.5)
    yway = int((total_gold_points % 7.5) // 1)
    point = round((total_gold_points % 1) * 10, 1)
    
    return {
        "kyat": kyat, 
        "pae": pae, 
        "yway": yway, 
        "point": point,
        "ratti": round(ratti, 2)
    }

def calculate_gold_price_comprehensive(kyat, pae, yway, point, gold_price):
    total_pae = (kyat * 16) + pae + (yway / 8) + (point / 80)
    gold_cost = (total_pae / 16) * gold_price
    return gold_cost

def calculate_gem_price(carat, price_per_carat, gold_weight_pae, gold_price):
    gem_cost = carat * price_per_carat
    # gold_weight_pae ကိုလည်း parameter အနေနဲ့ လက်ခံနိုင်အောင်ပြင်ထားသည်
    gold_cost = (gold_weight_pae / 16) * gold_price
    total_cost = gem_cost + gold_cost
    return gem_cost, gold_cost, total_cost
