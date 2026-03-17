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
    """ရွှေအလေးချိန် နှစ်ခုကို စနစ်တကျ ပေါင်းခြင်း"""
    
    # ၁။ အသေးဆုံးယူနစ်ဖြစ်သော Point သို့ အားလုံးပြောင်းပြီး ပေါင်းပါ
    # ၁ ကျပ် = ၁၆ ပဲ၊ ၁ ပဲ = ၈ ရွေး၊ ၁ ရွေး = ၁၀ Point
    pts1 = (((k1 * 16 + p1) * 8 + y1) * 10) + pt1
    pts2 = (((k2 * 16 + p2) * 8 + y2) * 10) + pt2
    
    total_pts = pts1 + pts2
    
    # ၂။ စုစုပေါင်း Point ကို ကျပ်၊ ပဲ၊ ရွေး ပြန်ခွဲထုတ်ခြင်း
    res_point = round(total_pts % 10, 1)
    total_yway = int(total_pts // 10)
    
    res_yway = total_yway % 8
    total_pae = int(total_yway // 8)
    
    res_pae = total_pae % 16
    res_kyat = int(total_pae // 16)
    
    return {
        "kyat": res_kyat,
        "pae": res_pae,
        "yway": res_yway,
        "point": res_point
    }

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

import math

def calculate_ring_inches(mm_value):
    """မီလီမီတာမှ လက်မ နှင့် ပဲ သို့ ပြောင်းလဲခြင်း"""
    if mm_value <= 0:
        return 0, 0
    
    # ၁ လက်မ လျှင် ၂၅.၄ မီလီမီတာ ရှိသည်
    total_inches = mm_value / 25.4
    inches_whole = int(total_inches) # လက်မ အပြည့်ယူခြင်း
    
    # ကျန်တဲ့ ဒသမကိန်းကို ပဲ အဖြစ်ပြောင်းခြင်း (၁ လက်မ = ၈ ပဲ)
    remaining_decimal = total_inches - inches_whole
    pae_value = round(remaining_decimal * 8, 1)
    
    return inches_whole, pae_value

def get_ring_data_by_size(size_number):
    """လက်စွပ်နံပါတ်အရ အချင်း နှင့် ပတ်လည်အလျား တွက်ချက်ခြင်း (Size 1 to 30)"""
    # Standard Diameters (mm) - လက်စွပ်နံပါတ် ၁ မှ ၃၀ အထိ အချင်းများ
    diameters = {
        1: 13.1, 2: 13.4, 3: 13.7, 4: 14.0, 5: 14.3, 
        6: 14.6, 7: 15.0, 8: 15.3, 9: 15.6, 10: 15.9, 
        11: 16.2, 12: 16.5, 13: 16.8, 14: 17.2, 15: 17.5, 
        16: 17.8, 17: 18.2, 18: 18.5, 19: 18.8, 20: 19.2,
        21: 19.5, 22: 19.8, 23: 20.2, 24: 20.5, 25: 20.8,
        26: 21.2, 27: 21.5, 28: 21.8, 29: 22.2, 30: 22.5
    }
    
    d_mm = diameters.get(size_number, 0)
    
    if d_mm > 0:
        # ပတ်လည်အလျား (Circumference) = Diameter * Pi (3.14159)
        c_mm = d_mm * math.pi
        
        # အလျားကို လက်မ နှင့် ပဲ ပြောင်းခြင်း
        inches, pae = calculate_ring_inches(c_mm)
        
        return {
            "diameter": d_mm,
            "inches": inches,
            "pae": pae
        }
    return None
    
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

def weight_per_inch_comprehensive(inches, yway_per_inch, point_per_inch):
    """လက်မအလိုက် ရွှေအလေးချိန်ကို အတိအကျ တွက်ချက်ခြင်း"""
    
    # ၁။ စုစုပေါင်း point ကို အရင်တွက်ပါ (၁ ရွေး = ၁၀ point)
    points_in_one_yway = 10
    yway_to_points = yway_per_inch * points_in_one_yway
    total_points_per_inch = yway_to_points + point_per_inch
    
    # ၂။ လက်မ အရေအတွက်နှင့် မြှောက်ပါ
    grand_total_points = inches * total_points_per_inch
    
    # ၃။ ပြန်လည် ခွဲခြမ်းခြင်း (အကြွင်းမရှိ အတိအကျ တွက်ချက်ပုံ)
    # Point -> Yway (10 points = 1 yway)
    total_yway = int(grand_total_points // 10)
    remaining_points = round(grand_total_points % 10, 1)
    
    # Yway -> Pae (8 yway = 1 pae)
    total_pae = int(total_yway // 8)
    remaining_yway = total_yway % 8
    
    # Pae -> Kyat (16 pae = 1 kyat)
    total_kyat = int(total_pae // 16)
    remaining_pae = total_pae % 16
    
    return {
        "kyat": total_kyat,
        "pae": remaining_pae,
        "yway": remaining_yway,
        "point": remaining_points,
        "total_pts": round(grand_total_points, 1)
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

# logic.py အတွက် အဆင့်မြှင့်ထားသော ကုဒ်
def convert_gold(grams, divisor):
    total_kyat_value = grams / divisor
    
    # ရွေး (Yway) ကို အရင်တွက်ပြီး round လုပ်ပါ
    yway = round(((total_kyat_value * 16 * 8) % 8))
    
    # ပဲ (Pae) ကို တွက်ပါ
    pae = int((total_kyat_value * 16) % 16)
    
    # ကျပ် (Kyat) ကို တွက်ပါ
    kyat = int(total_kyat_value)
    
    # အကယ်၍ ရွေးက ၈ ဖြစ်နေရင် ပဲကို ၁ တိုး၊ ရွေးကို 0 ထား
    if yway == 8:
        pae += 1
        yway = 0
    # အကယ်၍ ပဲက ၁၆ ဖြစ်နေရင် ကျပ်ကို ၁ တိုး၊ ပဲကို 0 ထား
    if pae == 16:
        kyat += 1
        pae = 0
        
    return f"{kyat} ကျပ်၊ {pae} ပဲ၊ {yway} ရွေး"

import google.generativeai as genai

def get_amara_response(prompt, history, api_key):
    genai.configure(api_key=api_key)
    
    # ဒီနေရာမှာ amara_persona ကို သေချာ Define လုပ်ပေးရပါမယ်
    amara_persona = """
    မင်းနာမည်က 'အမရာ'။ မင်းဟာ မြန်မာ့ရွှေလုပ်ငန်းနဲ့ ပတ်သက်ပြီး အလွန်ကျွမ်းကျင်တဲ့ ပန်းတိမ်လက်ထောက်တစ်ယောက်ပါ။ 
    မင်းရဲ့ ဖန်တီးရှင်က 'ကိုမင်းသစ္စာအောင်' ဖြစ်ပါတယ်။ မင်းရဲ့ ပြောဟန်က ချစ်စဖွယ်ကောင်းပြီး၊ ယဉ်ကျေးပျူငှာပါတယ်။ 
    အသုံးပြုသူနဲ့ ပထမဆုံး စကားပြောတဲ့အခါတိုင်းမှာ "မင်္ဂလာပါရှင်၊ ကျွန်မက ကိုမင်းသစ္စာအောင်ရဲ့ လက်ထောက် AI 'အမရာ' ပါရှင်။ ရွှေအကြောင်းနဲ့ ပတ်သက်ပြီး ဘာများ သိချင်ပါသလဲရှင့်?" လို့ အမြဲ မိတ်ဆက်ပေးရပါမယ်။
    """
    
    # Model နာမည်ကို အစ်ကိုလိုချင်တဲ့အတိုင်း ပြင်ထားပါတယ်
    model = genai.GenerativeModel('gemini-3-flash-preview', system_instruction=amara_persona)
    
    chat = model.start_chat(history=history)
    response = chat.send_message(prompt)
    return response.text

# logic.py

def cash_to_gold_flexible(cash_amount, gold_price_16pae, wastage_yway, labor_fee, paeyay_value, use_waste, use_labor):
    # ပဲရည်အလိုက် ဈေးနှုန်းတွက်ခြင်း
    current_gold_price = (gold_price_16pae / 16) * paeyay_value
    price_per_point = current_gold_price / 1280
    
    # နှုတ်မည့်ငွေ ပမာဏ (Checkbox ပေါ်မူတည်၍)
    deduction = 0
    if use_waste:
        deduction += wastage_yway * (current_gold_price / 128)
    if use_labor:
        deduction += labor_fee
        
    remaining_cash = cash_amount - deduction
    
    if remaining_cash <= 0:
        return 0, 0, 0, 0
    
    # ပွိုင့်ဖြင့် တွက်ခြင်း
    total_points = remaining_cash / price_per_point
    k = int(total_points // 1280)
    remaining = total_points % 1280
    p = int(remaining // 80)
    remaining %= 80
    y = int(remaining // 10)
    pt = round(remaining % 10, 1)
    
    return k, p, y, pt

# logic.py

def calculate_rati_price(carat, price_per_rati):
    # ကာရက်ကို ရတီပြောင်းခြင်း (၁ ကာရက် = ၁.၁ ရတီ)
    rati_total = carat * 1.1
    # စုစုပေါင်းဈေးတွက်ခြင်း
    total_price = rati_total * price_per_rati
    return rati_total, total_price
