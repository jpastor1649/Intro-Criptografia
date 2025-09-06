import secrets
import string


def generateRandomKey(length):
    if not isinstance(length, int):
        raise TypeError("Length must be an integer")
    if length <= 0:
        raise ValueError("Length must be positive")

    # Use printable ASCII characters for the key
    alphabet = string.ascii_letters + string.digits + string.punctuation + " "
    return "".join(secrets.choice(alphabet) for _ in range(length))


def otpEncrypt(txt, key):

    # Input validation
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
    
    # Input validation
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
    # Example usage with proper OTP implementation
    # plaintext = "Hello, World! This is a secret message."
    plaintext = input("Enter the plaintext message: ")

    # Generate a random key of the same length as the plaintext
    key = generateRandomKey(len(plaintext))

    print("=== One-Time Pad Encryption Example ===")
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print(f"Key length: {len(key)}")
    print()

    try:
        # Encrypt the plaintext
        ciphertext = otpEncrypt(plaintext, key)
        print(f"Ciphertext (bytes): {ciphertext}")
        print()

        # Decrypt the ciphertext
        decrypted = otpDecrypt(ciphertext, key)
        print(f"Decrypted: {decrypted}")
        print(f"Decryption successful: {plaintext == decrypted}")

    except (TypeError, ValueError) as e:
        print(f"Error: {e}")


