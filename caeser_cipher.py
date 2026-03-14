import string

def encrypt(text, key):
    encrypted_text = ""
    for char in text:
        if char in string.ascii_letters:
            shift = key % 26
            if char.islower():
                base = ord('a')
            else:
                base = ord('A')
            encrypted_char = chr((ord(char) - base + shift) % 26 + base)
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    return encrypted_text

def decrypt(text, key):
    decrypted_text = ""
    for char in text:
        if char in string.ascii_letters:
            shift = key % 26
            if char.islower():
                base = ord('a')
            else:
                base = ord('A')
            decrypted_char = chr((ord(char) - base - shift) % 26 + base)
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text

def brute_force_decrypt(text):
    for key in range(26):
        decrypted_text = decrypt(text, key)
        print(f"Key {key}: {decrypted_text}")

if __name__ == "__main__":
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Brute Force")
    choice = input("Choose an option: ")
    if choice == '1':
        text = input("Enter text to encrypt: ")
        key = int(input("Enter key: "))
        print("Encrypted text:", encrypt(text, key))
    elif choice == '2':
        text = input("Enter text to decrypt: ")
        key = int(input("Enter key: "))
        print("Decrypted text:", decrypt(text, key))
    elif choice == '3':
        text = input("Enter text to brute force decrypt: ")
        brute_force_decrypt(text)
    else:
        print("Invalid option.")