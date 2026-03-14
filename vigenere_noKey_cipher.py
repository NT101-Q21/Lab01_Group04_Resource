import os
from collections import Counter

# Tần suất xuất hiện chữ cái chuẩn trong tiếng Anh (A-Z)
ENGLISH_FREQ = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
    0.06094, 0.06966, 0.00015, 0.00772, 0.04025, 0.02406, 0.06749,
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074
]

def get_input_data():
    """Hàm xử lý luồng nhập dữ liệu (Bàn phím hoặc File)"""
    print("\n--- NHẬP CIPHERTEXT ---")
    choice = input("Bạn muốn nhập dữ liệu từ đâu? (1: Bàn phím, 2: File): ").strip()
    if choice == '1':
        return input("Nhập chuỗi văn bản (Ciphertext): ")
    elif choice == '2':
        filepath = input("Nhập đường dẫn file (VD: input.txt): ").strip()
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            print(f"Lỗi: Không tìm thấy file '{filepath}'.")
            return None
    else:
        print("Lựa chọn không hợp lệ.")
        return None

def clean_text(text):
    """Chuẩn hóa dữ liệu: Chỉ giữ lại ký tự alphabet và chuyển thành chữ HOA."""
    return "".join([c.upper() for c in text if c.isalpha()])

def calculate_ioc(text):
    """Tính Chỉ số trùng hợp (Index of Coincidence) cho một chuỗi văn bản."""
    n = len(text)
    if n <= 1: return 0
    freq = Counter(text)
    ioc = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
    return ioc

def find_key_length(cipher_text, max_len=20):
    """Tìm độ dài khóa dựa trên IoC trung bình của các cột."""
    avg_iocs = []
    
    for l in range(1, max_len + 1):
        columns = [cipher_text[i::l] for i in range(l)]
        avg_ioc = sum(calculate_ioc(col) for col in columns) / l
        avg_iocs.append((l, avg_ioc))

    possible_lengths = [x for x in avg_iocs if x[1] > 0.06]
    
    if possible_lengths:
        return possible_lengths[0] 
    else:
        return max(avg_iocs, key=lambda x: x[1])

def find_key(cipher_text, key_length):
    key = ""
    for i in range(key_length):
        # Lấy cột thứ i
        col = cipher_text[i::key_length]
        best_shift = 0
        min_chi_sq = float('inf')
        
        # Thử 26 độ dịch chuyển (Caesar) cho cột này
        for shift in range(26):
            # Dịch ngược cột lại 'shift' bước
            decrypted_col = "".join(chr(((ord(c) - 65 - shift) % 26) + 65) for c in col)
            freq = Counter(decrypted_col)
            
            # Tính sai số Chi-square so với tiếng Anh chuẩn
            chi_sq = 0
            for char_code in range(26):
                char = chr(char_code + 65)
                observed = freq.get(char, 0)
                expected = len(col) * ENGLISH_FREQ[char_code]
                if expected > 0:
                    chi_sq += ((observed - expected) ** 2) / expected
                    
            if chi_sq < min_chi_sq:
                min_chi_sq = chi_sq
                best_shift = shift
                
        key += chr(best_shift + 65)
    return key

def decrypt_vigenere(ciphertext, key):
    result = []
    key_index = 0
    key_length = len(key)
    
    key_upper = key.upper()
    k_values = [ord(k) - ord('A') for k in key_upper]
    
    for char in ciphertext:
        if char.isalpha():
            k_i = k_values[key_index % key_length]
            
            if char.isupper():
                c_i = ord(char) - ord('A')
                p_i = (c_i - k_i + 26) % 26
                result.append(chr(p_i + ord('A')))
            else:
                c_i = ord(char) - ord('a')
                p_i = (c_i - k_i + 26) % 26                
                result.append(chr(p_i + ord('a')))
                
            key_index += 1
        else:
            result.append(char)            
    return "".join(result)

def main():
    print("="*60)
    print(" CÔNG CỤ TỰ ĐỘNG PHÁ MÃ VIGENÈRE CIPHER (Ciphertext-Only) ")
    print("="*60)
    
    raw_text = get_input_data()
    if not raw_text:
        return
        
    print("\n[+] Đang chuẩn hóa dữ liệu...")
    cleaned_cipher = clean_text(raw_text)
    
    print("[+] Đang phân tích độ dài khóa bằng Index of Coincidence (IoC)...")
    key_length, ioc_score = find_key_length(cleaned_cipher)
    print(f"    -> Đoán độ dài khóa: {key_length} (IoC trung bình: {ioc_score:.4f})")
    
    print(f"[+] Đang phân tích tần suất (Chi-square) tìm {key_length} ký tự khóa...")
    guessed_key = find_key(cleaned_cipher, key_length)
    print(f"    -> TÌM THẤY KHÓA: '{guessed_key}'")
    
    print("\n[+] Đang tiến hành giải mã...")
    plaintext = decrypt_vigenere(raw_text, guessed_key)
    
    print("\n" + "="*60)
    print(" KẾT QUẢ BẢN RÕ (PLAINTEXT) ")
    print("="*60)
    print(plaintext)
    print("="*60)

if __name__ == "__main__":
    main()