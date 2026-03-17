import string

def create_matrix(key):
    key = key.upper().replace(" ", "").replace("J", "I")
    matrix = []
    used_letters = set()

    for char in key:
        if char not in used_letters and char in string.ascii_uppercase:
            matrix.append(char)
            used_letters.add(char)

    for char in string.ascii_uppercase:
        if char not in used_letters and char != 'J':
            matrix.append(char)

    return [matrix[i:i+5] for i in range(0, 25, 5)]


def print_matrix(matrix):
    print("\nMatrix:")
    for row in matrix:
        print(" ".join(row))


def process_text(text):
    text = text.upper().replace(" ", "").replace("J", "I")
    text = ''.join([c for c in text if c in string.ascii_uppercase])
    result = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = ""
        if i + 1 < len(text):
            b = text[i+1]
        if a == b:
            result += a + "X"
            i += 1
        else:
            if b:
                result += a + b
                i += 2
            else:
                result += a + "X"
                i += 1
    return result


def find_pos(matrix, char):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == char:
                return r, c


def encrypt(text, key):
    matrix = create_matrix(key)
    print_matrix(matrix)
    text = process_text(text)
    encrypted = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        r1, c1 = find_pos(matrix, a)
        r2, c2 = find_pos(matrix, b)

        if r1 == r2:
            encrypted += matrix[r1][(c1 + 1) % 5]
            encrypted += matrix[r2][(c2 + 1) % 5]
        elif c1 == c2:
            encrypted += matrix[(r1 + 1) % 5][c1]
            encrypted += matrix[(r2 + 1) % 5][c2]
        else:
            encrypted += matrix[r1][c2]
            encrypted += matrix[r2][c1]

    return encrypted


def decrypt(text, key):
    matrix = create_matrix(key)
    print_matrix(matrix)

    decrypted = ""

    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        r1, c1 = find_pos(matrix, a)
        r2, c2 = find_pos(matrix, b)

        if r1 == r2:
            decrypted += matrix[r1][(c1 - 1) % 5]
            decrypted += matrix[r2][(c2 - 1) % 5]
        elif c1 == c2:
            decrypted += matrix[(r1 - 1) % 5][c1]
            decrypted += matrix[(r2 - 1) % 5][c2]
        else:
            decrypted += matrix[r1][c2]
            decrypted += matrix[r2][c1]

    return decrypted

if __name__ == "__main__":
    print("1. Encrypt")
    print("2. Decrypt")
    choice = input("Choose: ")
    key = input("Enter key: ")

    if choice == '1':
        text = input("Enter plaintext: ")
        print("Ciphertext:", encrypt(text, key))

    elif choice == '2':
        text = input("Enter ciphertext: ")
        print("Plaintext:", decrypt(text, key))

    else:
        print("Invalid code")