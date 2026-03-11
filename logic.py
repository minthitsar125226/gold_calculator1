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

# --- ၃။ လက်စွပ်/လက်ကောက် Logic ---
def ring_no_to_mm(ring_no):
    return 11.63 + (ring_no * 0.8128)

def inch_pe_to_mm(inch, pe):
    return (inch + (pe / 16)) * 25.4

def mm_to_inch_pe(mm):
    total_inches = mm / 25.4
    inches = int(total_inches)
    pe = round((total_inches - inches) * 16)
    return inches, pe

def bangle_circumference(inch, pe):
    """အချင်းမှ ပတ်လည်အလျားတွက်ခြင်း"""
    d_mm = inch_pe_to_mm(inch, pe)
    return d_mm * 3.14159

# --- ၄။ အထည်ယူ/အပ် Logic ---
def job_comparison(give_total_pe, return_net_pe, wastage_pe):
    """ပေးရွှေ နှင့် (ပြန်အပ် + အလျော့) နှိုင်းယှဉ်ခြင်း"""
    total_return = return_net_pe + wastage_pe
    return give_total_pe - total_return
