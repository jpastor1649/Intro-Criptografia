"""
Author: jpastor
Date: 2025-09-06
One-Time Pad (OTP) Encryption and Decryption Example
"""

import secrets
import string


def generateRandomKey(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation + " "
    return "".join(secrets.choice(alphabet) for _ in range(length))


def otpEncrypt(txt, key):

    if not isinstance(txt, str):
        raise TypeError("Text must be a string")
    if not isinstance(key, str):
        raise TypeError("Key must be a string")

    txt_bytes = txt.encode("utf-8")
    key_bytes = key.encode("utf-8")

    if len(txt_bytes) != len(key_bytes):
        raise ValueError("Text and key must be of the same length")

    # XOR each byte in the text with the corresponding byte in the key
    ciphertxt = bytes([txt_bytes[i] ^ key_bytes[i] for i in range(len(txt_bytes))])
    return ciphertxt


def otpDecrypt(ciphertxt, key):

    if not isinstance(ciphertxt, bytes):
        raise TypeError("Ciphertext must be bytes, not string")
    if not isinstance(key, str):
        raise TypeError("Key must be a string")

    key_bytes = key.encode("utf-8")

    if len(ciphertxt) != len(key_bytes):
        raise ValueError("Ciphertext and key must be of the same length")

    # XOR each byte in the ciphertext with the corresponding byte in the key.
    txt_bytes = bytes([ciphertxt[i] ^ key_bytes[i] for i in range(len(ciphertxt))])
    return txt_bytes.decode("utf-8")


if __name__ == "__main__":
    plaintext = input("Enter the plaintext message: ")

    print("=== One-Time Pad Encryption Example ===")

    print(f"Plaintext: {plaintext}")
    choice = input("Do you want to provide your own key? (y/n): ").strip().lower()
    txt_bytes = plaintext.encode("utf-8")  
    if choice == "y":
        user_key = input("Enter your key: ")
        if len(user_key.encode("utf-8")) != len(txt_bytes):  
            print("Error: Key length must match plaintext length (in bytes).")
            exit(1)
        key = user_key
    else:
        key = generateRandomKey(len(txt_bytes))  
    print(f"Key: {key}")
    print(f"Key length (chars): {len(key)}")
    print(f"plaintext length (bytes): {len(txt_bytes)}")
    print()

    try:
        ciphertext = otpEncrypt(plaintext, key)
        print(f"Ciphertext (represented in hex): {ciphertext.hex()}")
        print()

        decrypted = otpDecrypt(ciphertext, key)
        print(f"Decrypted: {decrypted}")
        print(f"Decryption successful: {plaintext == decrypted}")

    except (TypeError, ValueError) as e:
        print(f"Error: {e}")
