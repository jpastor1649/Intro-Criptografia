import numpy as np


def rotate_grille(grille, direction=1):
    return np.rot90(grille, -1 if direction == 1 else 1)


def create_grille(size, holes):
    g = np.zeros((size, size), dtype=int)
    for r, c in holes:
        g[r][c] = 1
    return g


def encrypt_block(block, grille, size, direction):
    matrix = np.full((size, size), "", dtype=str)
    idx = 0
    g = grille.copy()
    for _ in range(4):
        for i in range(size):
            for j in range(size):
                if g[i][j] == 1 and idx < len(block):
                    matrix[i][j] = block[idx]
                    idx += 1
        g = rotate_grille(g, direction)
    return "".join(matrix.flatten())


def decrypt_block(block, grille, size, direction):
    matrix = np.array(list(block)).reshape(size, size)
    text = ""
    g = grille.copy()
    for _ in range(4):
        for i in range(size):
            for j in range(size):
                if g[i][j] == 1:
                    text += matrix[i][j]
        g = rotate_grille(g, direction)
    return text


def turning_grille(message, size, direction, mode, holes):
    message = message.replace(" ", "").upper()
    grille = create_grille(size, holes)
    total = size * size
    result = ""

    if mode == 1:  # Encrypt
        while len(message) % total != 0:
            message += "X"
        blocks = [message[i : i + total] for i in range(0, len(message), total)]
        for b in blocks:
            result += encrypt_block(b, grille, size, direction)
    else:  # Decrypt
        while len(message) % total != 0:
            message += "X"
        blocks = [message[i : i + total] for i in range(0, len(message), total)]
        for b in blocks:
            result += decrypt_block(b, grille, size, direction)
    return result


def show_grille(grille):
    print("\n".join(" ".join(str(x) for x in row) for row in grille))


# ---------------------------
# Example
# ---------------------------

size = 4
direction = 1  # 1 = clockwise
holes = [(0, 0), (2, 1), (2, 3), (3, 2)]  # valid 4x4 grille

message = "JIM ATTACKS AT DAWN"
show_grille(create_grille(size, holes))
encrypted = turning_grille(message, size, direction, 1, holes)
decrypted = turning_grille(encrypted, size, direction, 0, holes)

print("Original message :", message)
print("Encrypted text   :", encrypted)
print("Decrypted text   :", decrypted)


def main():
    """Main function for manual testing of the Turning Grille algorithm."""
    print("=== Turning Grille Algorithm ===")
    print()

    # Grid size
    size = int(input("Grid size (n for nxn): "))

    # Rotation direction
    print("\nRotation direction:")
    print("  1 = Clockwise")
    print("  0 = Counterclockwise")
    direction = int(input("Direction (1 or 0): "))

    # Mode
    print("\nOperation mode:")
    print("  1 = Encryption")
    print("  0 = Decryption")
    mode = int(input("Mode (1 or 0): "))

    # Hole positions
    print(f"\nEnter the hole positions for the {size}x{size} grid")
    print("Format: row,column (indexed from 0)")
    print("Example: 0,1 means row 0, column 1")
    print("Type 'done' to finish")

    holes = []
    while True:
        hole_input = input("Hole position (row,column) or 'done': ").strip()
        if hole_input.lower() == "done":
            break
        try:
            row, column = map(int, hole_input.split(","))
            if 0 <= row < size and 0 <= column < size:
                holes.append((row, column))
                print(f"  Hole added at position ({row}, {column})")
            else:
                print(
                    f"  Error: Position out of range. Must be between (0,0) and ({size-1},{size-1})"
                )
        except ValueError:
            print("  Error: Invalid format. Use row,column")

    if not holes:
        print("Error: You must enter at least one hole.")
        return

    print(f"\nConfigured holes: {holes}")

    # Show the grille
    grille = create_grille(size, holes)
    print(f"\nGrille (1 = hole, 0 = blocked):")
    show_grille(grille)

    # Message to encrypt/decrypt
    if mode == 1:
        message = input("\nMessage to encrypt: ").strip()
    else:
        message = input("\nMessage to decrypt: ").strip()

    # Process
    try:
        result = turning_grille(message, size, direction, mode, holes)

        print("\n=== RESULT ===")
        if mode == 1:
            print(f"Original message: {message}")
            print(f"Encrypted text:   {result}")
        else:
            print(f"Encrypted text:   {message}")
            print(f"Decrypted message: {result}")

    except Exception as e:
        print(f"Processing error: {e}")


if __name__ == "__main__":
    print("=== AUTOMATIC EXAMPLE ===")
    print()

    print("\n" + "=" * 50)
    main()
