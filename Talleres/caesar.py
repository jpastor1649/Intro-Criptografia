"""
Author: jpastor
Date: 2025-09-13
Caesar's Cipher Encryption and Decryption Example
"""


def caesar_encrypt(text, shifts):
    ciphertext = ""
    for char in text:
        if char.isalpha():
            # Determine if character is uppercase or lowercase
            base = ord("A") if char.isupper() else ord("a")
            # Shift character and wrap around the alphabet
            ciphertext += chr((ord(char) - base + shifts) % 26 + base)
        else:
            # Non-alphabetic characters are added unchanged
            ciphertext += char
    return ciphertext


def caesar_decrypt(ciphertext, shifts):
    # Decrypting is just encrypting with the negative shift
    return caesar_encrypt(ciphertext, -shifts)


if __name__ == "__main__":
    try:
        print("=== Caesar Cipher ===")

        choice = int(input("Do you want to encrypt (1) or decrypt (0)? "))
        if choice not in [0, 1]:
            print("Error: Enter 1 to encrypt or 0 to decrypt")
            exit(1)

        message = input("Enter the message: ").strip()
        if not message:
            print("Error: Message cannot be empty")
            exit(1)

        k = int(input("Enter the key (shift k): "))

        output = (
            caesar_encrypt(message, k) if choice == 1 else caesar_decrypt(message, k)
        )
        action = "encrypted" if choice == 1 else "decrypted"

        print("\n=== Result ===")
        print(f"Original message: {message}")
        print(f"{action.capitalize()} text: {output}")

    except ValueError as e:
        print(f"Error: {e}")
