import os

def normalize_key(key):
    return "".join([c.upper() for c in key if c.isalpha()])

def vigenere_cipher(text, key, mode='encrypt'):
    normalized_key = normalize_key(key)
    if not normalized_key:
        return "Lỗi: Khóa phải chứa ít nhất một chữ cái!"

    key_length = len(normalized_key)
    key_as_int = [ord(k) - ord('A') for k in normalized_key]
    
    result = []
    key_index = 0 
    
    for char in text:
        if char.isalpha():
            is_lower = char.islower()
            p = ord(char.upper()) - ord('A')
            k = key_as_int[key_index % key_length]
            
            if mode == 'encrypt':
                c = (p + k) % 26
            elif mode == 'decrypt':
                c = (p - k + 26) % 26
                
            result.append(chr(c + ord('A')))
            key_index += 1
        else:
            result.append(char)  
    return "".join(result)

def get_input_data():
    """Hàm xử lý luồng nhập dữ liệu của người dùng (Bàn phím hoặc File)"""
    choice = input("Bạn muốn nhập dữ liệu từ đâu? (1: Bàn phím, 2: File): ").strip()
    if choice == '1':
        return input("Nhập chuỗi văn bản: ")
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

def main():
    print("="*50)
    print(" CHƯƠNG TRÌNH MÃ HÓA/GIẢI MÃ VIGENÈRE CIPHER ")
    print("="*50)
    
    while True:
        print("\nCHỨC NĂNG:")
        print("1. Mã hóa (Encrypt)")
        print("2. Giải mã (Decrypt)")
        print("3. Thoát")
        
        action = input("Chọn chức năng (1/2/3): ").strip()
        
        if action == '3':
            print("Đã thoát chương trình.")
            break
            
        if action in ['1', '2']:
            text = get_input_data()
            if text is None:
                continue # Nếu lỗi đọc file, quay lại menu
                
            key = input("Nhập khóa bí mật (Key): ")
            mode = 'encrypt' if action == '1' else 'decrypt'
            
            result = vigenere_cipher(text, key, mode)
            
            print("\n--- KẾT QUẢ ---")
            print(result)
            print("-" * 15)
        else:
            print("Vui lòng chọn 1, 2 hoặc 3.")

if __name__ == "__main__":
    main()