"""
Author: jpastor
Date: 2025-09-20
Hill Cipher Encryption Example using a nxn key matrix it just works with letters not with numbers or special characters
Try it with key: [[11 8]
                 [3 7]]
"""

import numpy as np
from math import gcd


# PRIVATE METHODS
def _get_matrix_from_input() -> list[list[int]]:
    n = int(input("Enter the size of the key matrix (n for nxn): "))
    key = []
    print(
        f"Enter the key matrix row by row (each row should have {n} integers separated by spaces):"
    )
    for i in range(n):
        row = list(map(int, input(f"Row {i + 1}: ").strip().split()))
        if len(row) != n:
            raise ValueError(f"Each row must have exactly {n} integers.")
        key.append(row)
    return np.array(key)


def _mod_inverse(a, m):
    """Compute the modular inverse of a under modulo m using Extended Euclidean Algorithm."""
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return ValueError(f"Modular inverse does not exist for {a} mod {m}")


def _validate_key(key: list[list[int]]) -> None:
    """Validate that the key is a square matrix and invertible modulo 26."""
    key = np.array(key)
    det = int(round(np.linalg.det(key)))  # Determinant of the key matrix
    det_mod = det % 26
    if det_mod == 0 or gcd(det_mod, 26) != 1:
        raise ValueError("Key matrix is not invertible modulo 26")
    return key


def _minor(matrix, i, j):
    """Calculate the minor of a matrix by removing the i-th row and j-th column."""
    mat = np.delete(matrix, i, axis=0)  # Delete i-th row
    mat = np.delete(mat, j, axis=1)  # Delete j-th column
    return mat


def _cofactor_matrix(matrix):
    """Calculate the cofactor matrix of a square matrix."""
    n = matrix.shape[0]
    cof_matrix = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            minor_ij = _minor(matrix, i, j)
            cof_matrix[i, j] = ((-1) ** (i + j)) * int(round(np.linalg.det(minor_ij)))
    return cof_matrix


def _adjugate(matrix):
    """Calculate the adjugate of a square matrix."""
    return _cofactor_matrix(matrix).T


# PUBLIC METHODS
def hill_cipher_encrypt(text: str, key: list[list[int]]) -> str:
    key = _validate_key(key)
    """Encrypt the text using the Hill cipher with the provided key matrix"""
    case_flags = [ch.islower() for ch in text if ch.isalpha()]  # Save case style

    text = "".join(
        ch.upper() for ch in text if ch.isalpha()
    )  # Remove spaces/punctuation and normalize to uppercase for calculation
    n = len(key)  # size of the key matrix

    if len(text) % n != 0:
        text += "X" * (n - (len(text) % n))  # Padding with 'X' if necessary

    result = []
    # Convert text to numbers (A=0, B=1, ..., Z=25)
    text_num = [ord(c) - ord("A") for c in text]
    for i in range(0, len(text_num), n):

        block = np.array(
            text_num[i : i + n]
        )  # Create a block vector for the current segment of text

        encrypted_block = (
            np.dot(block, key) % 26
        )  # Encrypt the block using the key matrix
        result.extend(encrypted_block)

    encrypted_text = [
        chr(num + ord("A")) for num in result
    ]  # Convert numbers back to letters

    # Restore original case style
    final_text = "".join(
        ch.lower() if case_flags[i % len(case_flags)] else ch
        for i, ch in enumerate(encrypted_text)
    )

    return final_text


def hill_cipher_decrypt(ciphertext: str, key: list[list[int]]) -> str:
    """Decrypt the ciphertext using the Hill cipher with the provided key matrix,
    preserving the case (upper/lower) of each character."""
    # Save case style
    case_flags = [ch.islower() for ch in ciphertext if ch.isalpha()]

    # Remove spaces/punctuation and normalize to uppercase for calculation
    ciphertext = "".join(ch.upper() for ch in ciphertext if ch.isalpha())
    key = _validate_key(key)
    n = len(key)

    det = int(round(np.linalg.det(key)))  # Determinant of the key matrix
    det_mod = det % 26
    det_inv = _mod_inverse(det_mod, 26)  # Modular inverse of the determinant

    adj = _adjugate(key)  # Adjugate of the key matrix
    key_inv = ((det_inv * adj) % 26).astype(int)  # Inverse key matrix modulo 26

    text_num = [ord(c) - ord("A") for c in ciphertext]
    text = []

    for i in range(0, len(text_num), n):
        block = np.array(text_num[i : i + n])
        decrypted_block = np.dot(block, key_inv) % 26
        text.extend(decrypted_block)

    decrypted_text = [chr(num + ord("A")) for num in text]

    # Restore original case style
    final_text = "".join(
        ch.lower() if case_flags[i % len(case_flags)] else ch
        for i, ch in enumerate(decrypted_text)
    ).rstrip(
        "X"
    )  # remove padding

    return final_text


def main():
    """Main function to run the Hill cipher encryption/decryption."""
    print("=== Hill Cipher ===")

    # Input key
    key = _get_matrix_from_input()

    # Choose operation
    choice = input("Do you want to (E)ncrypt or (D)ecrypt? ").strip().upper()

    if choice == "E":
        text = input("Enter the text to encrypt: ")
        encrypted_text = hill_cipher_encrypt(text, key)
        print("\n=== Result ===")
        print("Original text :", text)
        print("Encrypted text:", encrypted_text)

    elif choice == "D":
        text = input("Enter the text to decrypt: ")
        decrypted_text = hill_cipher_decrypt(text, key)
        print("\n=== Result ===")
        print("Encrypted text:", text)
        print("Decrypted text:", decrypted_text)

    else:
        print("Invalid option. Please choose 'E' or 'D'.")


if __name__ == "__main__":
    main()
