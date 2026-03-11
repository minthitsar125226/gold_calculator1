# utils.py

def format_gold_weight(total_pe):
    if total_pe <= 0: return "၀ ကျပ်၊ ၀ ပဲ၊ ၀ ရွေး၊ ၀ Point"
    k = int(total_pe // 16)
    p = int(total_pe % 16)
    rem_pe = total_pe % 1
    total_points = round(rem_pe * 80)
    y = int(total_points // 10)
    pt = int(total_points % 10)
    return f"{k} ကျပ်၊ {p} ပဲ၊ {y} ရွေး၊ {pt} Point"

def calculate_pe(k, p, y, pt):
    return (k * 16) + p + (y / 8) + (pt / 80)

# to_pe ဆိုပြီးခေါ်ရင်လည်း calculate_pe ကိုပဲ သုံးအောင် လုပ်ထားပါတယ်
def to_pe(k, p, y, pt):
    return calculate_pe(k, p, y, pt)

def mm_to_inch_pe(mm):
    total_inches = mm / 25.4
    inches = int(total_inches)
    pe = round((total_inches - inches) * 16)
    return inches, pe

def inch_pe_to_mm(inch, pe):
    return (inch + (pe / 16)) * 25.4

def format_length_inches(total_inches):
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
    return f"{ft} ပေ {rem_in} လက်မ {pe} ပဲ"
