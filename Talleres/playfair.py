"""
Author: jpastor
Date: 2025-09-06
Playfair Cipher Encryption and Decryption Example"""

import string


def generate_key_matrix(key):
    key = key.upper().replace("J", "I")  # Normalize key
    matrix = []
    used = set()

    # Add letters from the key
    for ch in key:
        if ch in string.ascii_uppercase and ch not in used:
            matrix.append(ch)
            used.add(ch)

    # Complete with the rest of the alphabet
    for ch in string.ascii_uppercase:
        if ch == "J":  # skip J
            continue
        if ch not in used:
            matrix.append(ch)
            used.add(ch)

    # Convert to 5x5 matrix
    return [matrix[i : i + 5] for i in range(0, 25, 5)]


def format_text(text, for_encrypt=True):
    text = text.upper().replace("J", "I")
    text = "".join([ch for ch in text if ch in string.ascii_uppercase])

    if for_encrypt:
        i = 0
        formatted = ""
        while i < len(text):
            a = text[i]
            b = text[i + 1] if i + 1 < len(text) else "X"

            if a == b:
                formatted += a + "X"
                i += 1
            else:
                formatted += a + b
                i += 2

        if len(formatted) % 2 != 0:
            formatted += "X"
        return formatted
    else:
        # For decryption, just ensure pairs
        if len(text) % 2 != 0:
            text += "X"
        return text


def find_position(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)
    return None


def playfair(text, key, mode=1):
    """
    mode=1 → encrypt
    mode=0 → decrypt
    """
    if not text or not key:
        raise ValueError("Text and key cannot be empty")

    matrix = generate_key_matrix(key)
    text = format_text(text, for_encrypt=(mode == 1))
    result = ""

    for i in range(0, len(text), 2):
        a, b = text[i], text[i + 1]
        pos_a = find_position(matrix, a)
        pos_b = find_position(matrix, b)

        if pos_a is None or pos_b is None:
            raise ValueError(
                f"Character not found in matrix: {a if pos_a is None else b}"
            )

        row1, col1 = pos_a
        row2, col2 = pos_b

        if row1 == row2:
            # Same row
            if mode == 1:
                result += matrix[row1][(col1 + 1) % 5]
                result += matrix[row2][(col2 + 1) % 5]
            else:
                result += matrix[row1][(col1 - 1) % 5]
                result += matrix[row2][(col2 - 1) % 5]

        elif col1 == col2:
            # Same column
            if mode == 1:
                result += matrix[(row1 + 1) % 5][col1]
                result += matrix[(row2 + 1) % 5][col2]
            else:
                result += matrix[(row1 - 1) % 5][col1]
                result += matrix[(row2 - 1) % 5][col2]

        else:
            # Rectangle
            result += matrix[row1][col2]
            result += matrix[row2][col1]

    # Basic cleanup for decryption
    if mode == 0:
        # Remove X at the end if it's padding
        if result.endswith("X"):
            result = result[:-1]

    return result


if __name__ == "__main__":
    try:
        print("=== Playfair Cipher ===")
        key = input("Enter the key: ").strip()
        if not key:
            print("Error: Key cannot be empty")
            exit(1)

        choice = int(input("Do you want to encrypt (1) or decrypt (0)? "))
        if choice not in [0, 1]:
            print("Error: Enter 1 to encrypt or 0 to decrypt")
            exit(1)

        message = input("Enter the message: ").strip()
        if not message:
            print("Error: Message cannot be empty")
            exit(1)

        # Show the key matrix
        matrix = generate_key_matrix(key)
        print("\nKey matrix:")
        for row in matrix:
            print(" ".join(row))

        output = playfair(message, key, mode=choice)
        action = "encrypted" if choice == 1 else "decrypted"

        print(f"\n=== Result ===")
        print(f"Original message: {message}")
        print(f"{action.capitalize()} text: {output}")

    except ValueError as e:
        print(f"Error: {e}")
