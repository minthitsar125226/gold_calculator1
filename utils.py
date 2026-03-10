# utils.py

def format_gold_weight(total_pe):
    """ပဲယူနစ်မှ ကျပ်၊ ပဲ၊ ရွေး၊ Point သို့ ပြန်ပြောင်းပေးခြင်း"""
    if total_pe <= 0:
        return "၀ ကျပ်၊ ၀ ပဲ၊ ၀ ရွေး၊ ၀ Point"
    k = int(total_pe // 16)
    p = int(total_pe % 16)
    rem_pe = total_pe % 1
    total_points = round(rem_pe * 80)
    y = int(total_points // 10)
    pt = int(total_points % 10)
    
    pt_str = f"{pt} Point"
    if pt == 5:
        pt_str = "5 Point (တစ်ခြမ်း)"
    return f"{k} ကျပ်၊ {p} ပဲ၊ {y} ရွေး၊ {pt_str}"

def calculate_pe(k, p, y, pt):
    """Input အလေးချိန်များကို ပဲစနစ်သို့ ပြောင်းပေးခြင်း"""
    return (k * 16) + p + (y / 8) + (pt / 80)

def to_pe(k, p, y, pt):
    """ပဲယူနစ်သို့ ပြောင်းလဲခြင်း (ပေါင်း/နုတ် အတွက်)"""
    return (k * 16) + p + (y / 8) + (pt / 80)

def from_pe(total_pe):
    """ပဲယူနစ်မှ ကျပ်၊ ပဲ၊ ရွေး၊ Point သို့ ပြန်ပြောင်းခြင်း (Tuple)"""
    k = int(total_pe // 16)
    p = int(total_pe % 16)
    rem_pe = total_pe % 1
    total_points = round(rem_pe * 80)
    y = int(total_points // 10)
    pt = int(total_points % 10)
    return k, p, y, pt
