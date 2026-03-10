# utils.py

def format_gold_weight(total_pe):
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
    return (k * 16) + p + (y / 8) + (pt / 80)
    # utils.py

def to_pe(k, p, y, pt):
    """ကျပ်၊ ပဲ၊ ရွေး၊ Point တွေကို ပဲယူနစ်အဖြစ် ပြောင်းလဲခြင်း"""
    return (k * 16) + p + (y / 8) + (pt / 80)

def from_pe(total_pe):
    """ပဲယူနစ်ကို ကျပ်၊ ပဲ၊ ရွေး၊ Point သို့ ပြန်ပြောင်းခြင်း"""
    k = int(total_pe // 16)
    p = int(total_pe % 16)
    rem_pe = total_pe % 1
    total_points = round(rem_pe * 80)
    y = int(total_points // 10)
    pt = int(total_points % 10)
    return k, p, y, pt
