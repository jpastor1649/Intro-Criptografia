import string


def generateKeyMatrix(key):
    matrix = []
    used_chars = set()
    key = key.upper().replace("J", "I")  # Treat 'I' and 'J' as the same letter

    for ch in key:
        if ch in string.ascii_uppercase and ch not in used_chars:
            used_chars.add(ch)
            matrix.append(ch)
    for ch in string.ascii_uppercase:
        if ch == "J":
            continue
        if ch not in used_chars:
            matrix.append(ch)
            used_chars.add(ch)

    matrix_2d = [matrix[i : i + 5] for i in range(0, 25, 5)]
    return matrix_2d
