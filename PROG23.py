def justify(text, width):
    words = text.split()
    lines = []
    current = []
    length = 0

    for word in words:
        # Check if word fits with current line
        if length + len(word) + len(current) <= width:
            current.append(word)
            length += len(word)
        else:
            lines.append(make_line(current, width))
            current = [word]
            length = len(word)

    # Last line is NOT justified
    if current:
        lines.append(" ".join(current))

    return "\n".join(lines)


def make_line(words, width):
    # One-word line
    if len(words) == 1:
        return words[0]

    total_letters = sum(len(word) for word in words)
    total_spaces = width - total_letters
    gaps = len(words) - 1

    # Minimum spaces per gap
    spaces = total_spaces // gaps

    # Extra spaces go into gaps from left to right
    extra = total_spaces % gaps

    line = ""

    for i in range(gaps):
        line += words[i]

        gap_size = spaces

        if i < extra:
            gap_size += 1

        line += " " * gap_size

    line += words[-1]

    return line
