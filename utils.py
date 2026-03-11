# utils.py

def format_gold_weight(total_pe):
    """ပဲ ယူနစ်မှ ကျပ်၊ ပဲ၊ ရွေး၊ Point သို့ ပြောင်းလဲခြင်း"""
    if total_pe <= 0: return "၀ ကျပ်၊ ၀ ပဲ၊ ၀ ရွေး၊ ၀ Point"
    k = int(total_pe // 16)
    p = int(total_pe % 16)
    rem_pe = total_pe % 1
    total_points = round(rem_pe * 80)
    y = int(total_points // 10)
    pt = int(total_points % 10)
    return f"{k} ကျပ်၊ {p} ပဲ၊ {y} ရွေး၊ {pt} Point"

def format_length_inches(total_inches):
    """လက်မမှ ပေ၊ လက်မ၊ ပဲ သို့ ပြောင်းလဲခြင်း"""
    if total_inches <= 0: return "၀ ပေ၊ ၀ လက်မ၊ ၀ ပဲ"
    ft = int(total_inches // 12)
    rem_in = int(total_inches % 12)
    pe = round((total_inches % 1) * 16)
    if pe >= 16:
        rem_in += 1
        pe -= 16
    if rem_in >= 12:
        ft += 1
        rem_in -= 12
    return f"{ft} ပေ၊ {rem_in} လက်မ၊ {pe} ပဲ"

def calculate_pe(k, p, y, pt):
    """ကျပ်၊ ပဲ၊ ရွေး၊ Point မှ ပဲ ယူနစ်သို့ ပြောင်းခြင်း"""
    return (k * 16) + p + (y / 8) + (pt / 80)

def to_pe(k, p, y, pt):
    """calculate_pe နှင့် အတူတူပင်ဖြစ်သည်"""
    return calculate_pe(k, p, y, pt)
