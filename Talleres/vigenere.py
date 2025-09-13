"""
Author: jpastor
Date: 2025-09-14
Vigenere Cipher Encryption and Decryption Example
"""


def expand_key_with_t(key, t, length):
    # Expand the key by repeating each character t times
    expanded = []
    for i in range(0, length, t):
        expanded.extend(list(key))
    return "".join(expanded)[:length]


def vigenere_encrypt(text, key, t):
    # Expand the key to match the length of the text
    expanded_key = expand_key_with_t(key, t, len(text))
    result = []
    for i, char in enumerate(text):
        if char.isalpha():
            # Determine if character is uppercase or lowercase
            base = ord("A") if char.isupper() else ord("a")
            # Calculate the shift based on the expanded key
            shift = ord(expanded_key[i].upper()) - ord("A")
            # Shift character and wrap around the alphabet
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)
    return "".join(result)


def vigenere_decrypt(ciphertext, key, t):
    # Expand the key to match the length of the ciphertext
    expanded_key = expand_key_with_t(key, t, len(ciphertext))
    result = []
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            # Determine if character is uppercase or lowercase
            base = ord("A") if char.isupper() else ord("a")
            # Calculate the shift based on the expanded key
            shift = ord(expanded_key[i].upper()) - ord("A")
            # Reverse shift character and wrap around the alphabet
            result.append(chr((ord(char) - base - shift) % 26 + base))
        else:
            result.append(char)
    return "".join(result)


if __name__ == "__main__":
    print("=== Vigenère Cipher with parameter t ===")

    key = input("Enter the key: ").strip().upper()
    text = input("Enter the text: ").replace(" ", "").upper()
    t = int(input("Enter the parameter t: ").strip())

    choice = input("Do you want to encrypt (E) or decrypt (D)? ").strip().lower()

    if choice == "e":
        result = vigenere_encrypt(text, key, t)
        print("\n=== Result ===")
        print("Original text :", text)
        print("Encrypted text:", result)
    elif choice == "d":
        result = vigenere_decrypt(text, key, t)
        print("\n=== Result ===")
        print("Encrypted text:", text)
        print("Decrypted text:", result)
    else:
        print("Invalid option. Use 'E' to encrypt or 'D' to decrypt.")
