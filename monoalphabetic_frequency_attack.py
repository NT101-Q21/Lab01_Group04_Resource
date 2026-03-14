import string
import random
from collections import Counter
import re

alphabet = list(string.ascii_uppercase)
english_order = list("ETAOINSHRDLCUMWFGYPBVKJXQZ")

# ==========================================
# BỘ TỪ ĐIỂN CHẤM ĐIỂM (KIẾN THỨC NGÔN NGỮ)
# ==========================================

# 1. Các từ phổ biến
common_words = [
    "THE", "AND", "TO", "OF", "A", "I", "IN", "WAS", "HE", "THAT", "IT", "HIS", "HER", 
    "YOU", "AS", "HAD", "WITH", "FOR", "SHE", "NOT", "AT", "BUT", "BE", "MY", "ON", 
    "HAVE", "HIM", "IS", "SAID", "ME", "WHICH", "BY", "SO", "THIS", "ALL", "FROM", 
    "THEY", "NO", "WERE", "IF", "WOULD", "OR", "WHEN", "WHAT", "THERE", "BEEN", "ONE", 
    "COULD", "VERY", "AN", "WHO", "MORE", "OUT", "UP", "THEIR", "ABOUT", "WHO", "WILL",
    "MANY", "THEN", "THEM", "THESE", "SOME", "MAKE", "LIKE", "INTO", "TIME", "HAS", 
    "LOOK", "TWO", "SEE", "WAY", "PEOPLE", "THAN", "FIRST", "WATER", "BECAUSE", "WHERE",
    "MOST", "SCHOOL", "YOUNG", "BOOKS", "SEVEN", "SERIES", "LIFE", "BOY"
]

common_quadgrams = ["THAT", "THER", "WITH", "TION", "HERE", "OULD", "IGHT", "HAVE", "WHIC", "THEI", "OVER", "FROM", "THIS", "THEY", "WERE", "SOME", "WHAT", "PROB", "OUNT", "MENT", "ALLY", "SCHO", "CHOO"]
common_trigrams = ["THE", "AND", "THA", "ENT", "ING", "ION", "TIO", "FOR", "NDE", "HAS", "NCE", "EDT", "TIS", "OFT", "MEN", "HER", "ERE", "HAT", "ATE", "PRO", "POP", "WIZ"]
common_bigrams = ["TH", "HE", "IN", "ER", "AN", "RE", "ON", "AT", "EN", "ND", "TI", "ES", "OR", "TE", "OF", "ED", "IS", "IT", "AL", "AR", "ST", "TO", "NT", "NG", "SE", "HA", "AS", "OU", "IO", "LE", "VE", "CO", "ME", "DE", "HI", "RI", "RO", "IC", "NE", "EA", "RA", "CE", "SP", "OP", "PO"]

# 3. LUẬT PHẠT
impossible_bigrams = [
    "CJ","CV","CX","DX","FQ","FX","GQ","GX","HX","JC","JQ","JX","JZ","KQ","KX","MX",
    "PX","PZ","QB","QC","QD","QF","QG","QH","QJ","QK","QL","QM","QN","QO","QP","QR",
    "QS","QT","QV","QW","QX","QY","QZ","SX","TQ","TX","VX","VW","VZ","WQ","WX","XJ",
    "ZJ","ZQ","ZX","VH","VK","VP","VQ","VR", "IJ", "IY", "XK", "ZK", "RX", "RZ",
    "SZ", "ZS", "QA", "QE", "QI" 
]

def create_initial_key(cipher_text):
    letters_only = [c.upper() for c in cipher_text if c.upper() in alphabet]
    freq = Counter(letters_only)
    order = [x[0] for x in freq.most_common()]
    
    key = {}
    for i, c in enumerate(order):
        if i < len(english_order):
            key[c] = english_order[i]
            
    unused_plain = [c for c in english_order if c not in key.values()]
    for c in alphabet:
        if c not in key:
            key[c] = unused_plain.pop(0)
    return key

def decrypt(cipher_text, key):
    plain = ""
    for c in cipher_text:
        if c.isupper():
            plain += key.get(c, c)
        elif c.islower():
            plain += key.get(c.upper(), c.upper()).lower()
        else:
            plain += c
    return plain

def score_text(plain_text):
    text_with_spaces = " " + re.sub(r'[^A-Z\s]', '', plain_text.upper()) + " "
    text_letters = re.sub(r'[^A-Z]', '', plain_text.upper())
    score = 0
    
    for bad_bg in impossible_bigrams:
        score -= text_letters.count(bad_bg) * 100
    
    for bg in common_bigrams:
        score += text_letters.count(bg) * 2
    for tg in common_trigrams:
        score += text_letters.count(tg) * 5
    for qg in common_quadgrams:
        score += text_letters.count(qg) * 10
        
    for w in common_words:
        score += text_with_spaces.count(f" {w} ") * 30
    return score

def improve_key(cipher_text, current_key, iterations=4000):
    best_key = current_key.copy()
    best_plain = decrypt(cipher_text, best_key)
    best_score = score_text(best_plain)
    
    for _ in range(iterations):
        new_key = best_key.copy()
        a, b = random.sample(alphabet, 2)
        new_key[a], new_key[b] = new_key[b], new_key[a]
        
        new_plain = decrypt(cipher_text, new_key)
        new_score = score_text(new_plain)
        
        if new_score > best_score:
            best_key = new_key
            best_plain = new_plain
            best_score = new_score
    return best_key, best_plain, best_score

def break_cipher(cipher_text, restarts=15):
    best_overall_plain = ""
    best_overall_score = -999999
    
    print("Đang chạy phân tích ngôn ngữ học chuyên sâu")
    base_key = create_initial_key(cipher_text)
    
    for i in range(restarts):
        current_key = base_key.copy()
        if i > 0:
            for _ in range(15):
                a, b = random.sample(alphabet, 2)
                current_key[a], current_key[b] = current_key[b], current_key[a]
                
        _, plain, score = improve_key(cipher_text, current_key, iterations=4000)
        
        if score > best_overall_score:
            best_overall_score = score
            best_overall_plain = plain
            
    return best_overall_plain

def main():
    cipher = input("Nhập ciphertext: ")
    result = break_cipher(cipher)
    print("\n--- PLAINTEXT DỰ ĐOÁN TỐT NHẤT ---")
    print(result)

if __name__ == "__main__":
    main()