import random

"""
Author: jpastor
Date: 2025-10-04
Homophonic Substitution Cipher Example
This implementation creates a homophonic substitution cipher where each letter can be mapped to multiple numbers.
"""


def gen_layout(m=100, n=26, seed=23):
    """Generate a random layout mapping letters to multiple numbers."""
    random.seed(seed)
    numbers = list(range(m))
    # Shuffle the numbers to create a random mapping
    random.shuffle(numbers)

    layout = {}
    step = m // n  # amount of numbers per letter
    letters = [chr(i) for i in range(65, 65 + n)]

    start = 0
    for letter in letters:
        end = start + step
        # Assign a slice of numbers to the letter
        layout[letter] = numbers[start:end]
        start = end
    return layout


def encrypt(message, layout):
    """Encrypt the message using the provided layout."""
    message = message.upper()
    cipher = []
    for ch in message:
        if ch in layout:
            # Randomly choose one of the possible numbers for the letter
            cipher.append(str(random.choice(layout[ch])))
        elif ch == " ":
            cipher.append(" ")
        else:
            continue
    return " ".join(cipher)


def decrypt(cipher, layout):
    """Decrypt the cipher using the provided layout."""
    # Create inverse mapping
    inverse = {}
    for letter, nums in layout.items():
        for n in nums:
            # If a number maps to multiple letters, the last one will be used
            inverse[str(n)] = letter

    parts = cipher.split()
    text = ""
    for p in parts:
        if p in inverse:
            text += inverse[p]
        else:
            text += " "
    return text


def main():
    """Main function to run the Homophonic Substitution cipher encryption/decryption."""
    print("=== Homophonic Substitution Cipher ===")

    # Generate layout with default parameters
    print("Generating layout with 100 numbers for 26 letters...")
    layout = gen_layout(m=100, n=26)

    # Option to show the layout
    show_layout = input("Do you want to see the layout? (Y/N): ").strip().upper()
    if show_layout == "Y":
        print("\nGenerated Layout:")
        for k, v in layout.items():
            print(f"{k}: {v}")
        print()

    # Choose operation
    choice = input("Do you want to (E)ncrypt or (D)ecrypt? ").strip().upper()

    if choice == "E":
        text = input("Enter the text to encrypt: ").strip()
        encrypted_text = encrypt(text, layout)
        print("\n=== Result ===")
        print("Original text :", text)
        print("Encrypted text:", encrypted_text)

    elif choice == "D":
        text = input(
            "Enter the encrypted text to decrypt (numbers separated by spaces): "
        ).strip()
        decrypted_text = decrypt(text, layout)
        print("\n=== Result ===")
        print("Encrypted text:", text)
        print("Decrypted text:", decrypted_text)

    else:
        print("Invalid option. Please choose 'E' or 'D'.")


if __name__ == "__main__":
    main()
