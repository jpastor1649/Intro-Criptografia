import base64
from pyDes import des, CBC, PAD_PKCS5


def image_cipher_des(path: str):

    print("=== DES image encryption ===")

    # 1️ Read the image in binary mode
    with open(path, "rb") as f:
        data = f.read()

    print(f"File size read: {len(data)} bytes")

    # 2️ Convert the file bytes to an array/list of bits (0/1)
    bits_list = [int(b) for byte in data for b in format(byte, "08b")]
    print(f"Total bits: {len(bits_list)}")
    print("First 64 bits: " + "".join(str(bit) for bit in bits_list[:64]))

    # 3 Create the DES cipher
    key = input("Enter an 8-character key (e.g., 'key12345'): ")
    if len(key) != 8:
        raise ValueError("The key must be exactly 8 characters.")

    iv = b"\x00" * 8  # initialization vector
    cipher = des(key.encode("utf-8"), CBC, iv, padmode=PAD_PKCS5)

    # 4 Encrypt the original bytes
    data_ciphered = cipher.encrypt(data)

    # 5 Encode to Base64 for display or transport as text
    data_base64_encoded = base64.b64encode(data_ciphered).decode("utf-8")
    print("\n=== Ciphertext (Base64) ===")
    print(data_base64_encoded[:100])
    print("... (output truncated) ...")
    print("===========================")

    with open("cipher_base64.txt", "w") as f:
        f.write(data_base64_encoded)
    print("🔒 Base64 saved in 'cipher_base64.txt'")

    return data_base64_encoded


def image_decipher_des(
    data_base64: str, key: str, output_path: str = "deciphered_image.png"
):

    if len(key) != 8:
        raise ValueError("The key must be exactly 8 characters (8 bytes).")

    # 1️ Initialize the DES cipher
    iv = b"\x00" * 8  # Initialization vector
    cipher = des(key.encode("utf-8"), CBC, iv, padmode=PAD_PKCS5)

    # 2️ Decode from Base64 to encrypted bytes
    data_ciphered = base64.b64decode(data_base64)

    # 3️ Decrypt the bytes
    data_deciphered = cipher.decrypt(data_ciphered)

    # 4️ Save the decrypted image
    with open(output_path, "wb") as f:
        f.write(data_deciphered)

    print(f"✅ Decrypted image saved as: {output_path}")
    return data_deciphered


def main():
    print("=== DES Image Cipher ===")
    option = input(
        "Choose an option:\n1. Cipher an image\n2. Decipher an image\nEnter 1 or 2: "
    )

    if option == "1":
        # Encrypt image
        data_base64 = image_cipher_des(
            input("Enter the path to the image file to encrypt: ")
        )

    elif option == "2":
        # Decrypt image
        key = input("Enter the 8-character key used for encryption: ")

        # Read Base64 text from file
        with open(input("Enter the path to the Base64 file: "), "r") as f:
            data_base64 = f.read()

        image_decipher_des(data_base64=data_base64, key=key)

    else:
        print("Invalid option. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
