def calc(expression):
    s = expression.replace(" ", "")
    i = 0

    def parse_expression():
        nonlocal i
        value = parse_term()

        while i < len(s) and s[i] in "+-":
            op = s[i]
            i += 1
            right = parse_term()

            if op == "+":
                value += right
            else:
                value -= right

        return value

    def parse_term():
        nonlocal i
        value = parse_factor()

        while i < len(s) and s[i] in "*/":
            op = s[i]
            i += 1
            right = parse_factor()

            if op == "*":
                value *= right
            else:
                value /= right

        return value

    def parse_factor():
        nonlocal i

        # Unary minus
        if s[i] == "-":
            i += 1
            return -parse_factor()

        # Unary plus (optional but harmless)
        if s[i] == "+":
            i += 1
            return parse_factor()

        # Parenthesized expression
        if s[i] == "(":
            i += 1
            value = parse_expression()
            i += 1  # skip ')'
            return value

        # Number
        start = i

        while i < len(s) and (s[i].isdigit() or s[i] == "."):
            i += 1

        return float(s[start:i])

    return parse_expression()
