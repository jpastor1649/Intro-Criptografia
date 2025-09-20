"""
Author: jpastor
Date: 2025-09-20
Hill Cipher implemented as a class.
Works only with letters A-Z (not numbers or special characters).
"""

import numpy as np
from math import gcd


class HillCipher:
    def __init__(self, key: list[list[int]]):
        """Initialize HillCipher with a given key matrix."""
        self.key = self._validate_key(np.array(key))
        self.n = len(self.key)

    # ---------- PRIVATE METHODS ----------
    def _mod_inverse(self, a: int, m: int) -> int:
        """Compute modular inverse of a modulo m using Extended Euclidean Algorithm."""
        a = a % m
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        raise ValueError(f"No modular inverse exists for {a} mod {m}")

    def _validate_key(self, key: np.ndarray) -> np.ndarray:
        """Validate key is a square matrix and invertible modulo 26."""
        det = int(round(np.linalg.det(key)))
        det_mod = det % 26
        if det_mod == 0 or gcd(det_mod, 26) != 1:
            raise ValueError("Key matrix is not invertible modulo 26")
        return key

    def _minor(self, matrix: np.ndarray, i: int, j: int) -> np.ndarray:
        """Compute minor of a matrix by removing row i and column j."""
        mat = np.delete(matrix, i, axis=0)
        mat = np.delete(mat, j, axis=1)
        return mat

    def _cofactor_matrix(self, matrix: np.ndarray) -> np.ndarray:
        """Compute cofactor matrix of a square matrix."""
        n = matrix.shape[0]
        cof_matrix = np.zeros((n, n), dtype=int)
        for i in range(n):
            for j in range(n):
                minor_ij = self._minor(matrix, i, j)
                cof_matrix[i, j] = ((-1) ** (i + j)) * int(round(np.linalg.det(minor_ij)))
        return cof_matrix

    def _adjugate(self, matrix: np.ndarray) -> np.ndarray:
        """Compute adjugate (transpose of cofactor matrix)."""
        return self._cofactor_matrix(matrix).T

    def _process_text(self, text: str) -> tuple[list[int], list[bool]]:
        """Convert text to numbers and save case flags."""
        case_flags = [ch.islower() for ch in text if ch.isalpha()]
        clean_text = "".join(ch.upper() for ch in text if ch.isalpha())
        if len(clean_text) % self.n != 0:
            clean_text += "X" * (self.n - (len(clean_text) % self.n))  # Padding
        text_num = [ord(c) - ord("A") for c in clean_text]
        return text_num, case_flags

    def _restore_case(self, letters: list[str], case_flags: list[bool]) -> str:
        """Restore original case to output text."""
        return "".join(
            ch.lower() if case_flags[i % len(case_flags)] else ch
            for i, ch in enumerate(letters)
        )

    # ---------- PUBLIC METHODS ----------
    def encrypt(self, text: str) -> str:
        """Encrypt text using Hill cipher with the key matrix."""
        text_num, case_flags = self._process_text(text)
        result = []

        for i in range(0, len(text_num), self.n):
            block = np.array(text_num[i : i + self.n])
            encrypted_block = np.dot(block, self.key) % 26
            result.extend(encrypted_block)

        encrypted_letters = [chr(num + ord("A")) for num in result]
        return self._restore_case(encrypted_letters, case_flags)

    def decrypt(self, ciphertext: str) -> str:
        """Decrypt text using Hill cipher with the key matrix."""
        text_num, case_flags = self._process_text(ciphertext)

        det = int(round(np.linalg.det(self.key)))
        det_mod = det % 26
        det_inv = self._mod_inverse(det_mod, 26)

        adj = self._adjugate(self.key)
        key_inv = ((det_inv * adj) % 26).astype(int)

        result = []
        for i in range(0, len(text_num), self.n):
            block = np.array(text_num[i : i + self.n])
            decrypted_block = np.dot(block, key_inv) % 26
            result.extend(decrypted_block)

        decrypted_letters = [chr(num + ord("A")) for num in result]
        return self._restore_case(decrypted_letters, case_flags)


# ---------- MAIN ----------
def main():
    print("=== Hill Cipher (OOP Version) ===")
    n = int(input("Enter the size of the key matrix (n for nxn): "))
    key = []
    print(f"Enter the key matrix row by row (each row should have {n} integers separated by spaces):")
    for i in range(n):
        row = list(map(int, input(f"Row {i + 1}: ").split()))
        if len(row) != n:
            raise ValueError(f"Row {i + 1} must have exactly {n} integers.")
        key.append(row)

    cipher = HillCipher(key)

    choice = input("Do you want to (E)ncrypt or (D)ecrypt? ").strip().upper()
    if choice == "E":
        text = input("Enter the text to encrypt: ")
        print("Encrypted text:", cipher.encrypt(text))
    elif choice == "D":
        text = input("Enter the text to decrypt: ")
        print("Decrypted text:", cipher.decrypt(text))
    else:
        print("Invalid option. Choose 'E' or 'D'.")


if __name__ == "__main__":
    main()
