def whitespace(code, inp=""):
    # Keep only meaningful Whitespace characters
    code = ''.join(c for c in code if c in ' \t\n')

    stack = []
    heap = {}
    calls = []
    output = []
    instructions = []
    labels = {}

    i = 0

    def number():
        nonlocal i

        if i >= len(code) or code[i] == '\n':
            raise ValueError("Invalid number")

        sign = -1 if code[i] == '\t' else 1
        i += 1

        bits = []

        while i < len(code) and code[i] != '\n':
            if code[i] == ' ':
                bits.append('0')
            elif code[i] == '\t':
                bits.append('1')
            else:
                raise ValueError("Invalid number")
            i += 1

        if i >= len(code):
            raise ValueError("Unterminated number")

        i += 1  # consume LF

        value = int(''.join(bits), 2) if bits else 0
        return sign * value

    def label():
        nonlocal i

        chars = []

        while i < len(code) and code[i] != '\n':
            chars.append(code[i])
            i += 1

        if i >= len(code):
            raise ValueError("Unterminated label")

        i += 1
        return ''.join(chars)

    # -------------------------------------------------------
    # PARSER
    # -------------------------------------------------------

    while i < len(code):
        imp = code[i]
        i += 1

        # ================= STACK =================
        if imp == ' ':
            if i >= len(code):
                raise ValueError("Invalid stack instruction")

            c = code[i]
            i += 1

            # Push
            if c == ' ':
                instructions.append(('push', number()))

            elif c == '\t':
                if i >= len(code):
                    raise ValueError("Invalid stack instruction")

                c2 = code[i]
                i += 1

                # Copy nth
                if c2 == ' ':
                    instructions.append(('copy', number()))

                # Slide
                elif c2 == '\n':
                    instructions.append(('slide', number()))

                else:
                    raise ValueError("Invalid stack instruction")

            elif c == '\n':
                if i >= len(code):
                    raise ValueError("Invalid stack instruction")

                c2 = code[i]
                i += 1

                if c2 == ' ':
                    instructions.append(('dup',))
                elif c2 == '\t':
                    instructions.append(('swap',))
                elif c2 == '\n':
                    instructions.append(('pop',))
                else:
                    raise ValueError("Invalid stack instruction")

            else:
                raise ValueError("Invalid stack instruction")

        # ================= TAB IMP =================
        elif imp == '\t':
            if i >= len(code):
                raise ValueError("Invalid instruction")

            second = code[i]
            i += 1

            # ---------------- Arithmetic ----------------
            if second == ' ':
                if i + 1 >= len(code):
                    raise ValueError("Invalid arithmetic instruction")

                op = code[i:i + 2]
                i += 2

                operations = {
                    '  ': 'add',
                    ' \t': 'sub',
                    ' \n': 'mul',
                    '\t ': 'div',
                    '\t\t': 'mod'
                }

                if op not in operations:
                    raise ValueError("Invalid arithmetic instruction")

                instructions.append((operations[op],))

            # ---------------- Heap ----------------
            elif second == '\t':
                if i >= len(code):
                    raise ValueError("Invalid heap instruction")

                c = code[i]
                i += 1

                if c == ' ':
                    instructions.append(('store',))
                elif c == '\t':
                    instructions.append(('retrieve',))
                else:
                    raise ValueError("Invalid heap instruction")

            # ---------------- I/O ----------------
            elif second == '\n':
                if i + 1 >= len(code):
                    raise ValueError("Invalid IO instruction")

                op = code[i:i + 2]
                i += 2

                operations = {
                    '  ': 'outchar',
                    ' \t': 'outnum',
                    '\t ': 'inchar',
                    '\t\t': 'innum'
                }

                if op not in operations:
                    raise ValueError("Invalid IO instruction")

                instructions.append((operations[op],))

            else:
                raise ValueError("Invalid instruction")

        # ================= FLOW CONTROL =================
        elif imp == '\n':
            if i + 1 >= len(code):
                raise ValueError("Invalid flow instruction")

            op = code[i:i + 2]
            i += 2

            if op == '  ':
                instructions.append(('label', label()))

            elif op == ' \t':
                instructions.append(('call', label()))

            elif op == ' \n':
                instructions.append(('jump', label()))

            elif op == '\t ':
                instructions.append(('jz', label()))

            elif op == '\t\t':
                instructions.append(('jn', label()))

            elif op == '\t\n':
                instructions.append(('ret',))

            elif op == '\n\n':
                instructions.append(('end',))

            else:
                raise ValueError("Invalid flow instruction")

        else:
            raise ValueError("Invalid IMP")

    # -------------------------------------------------------
    # BUILD LABEL TABLE
    # -------------------------------------------------------

    for pos, inst in enumerate(instructions):
        if inst[0] == 'label':
            name = inst[1]

            if name in labels:
                raise ValueError("Duplicate label")

            labels[name] = pos

    # Validate referenced labels
    for inst in instructions:
        if inst[0] in ('call', 'jump', 'jz', 'jn'):
            if inst[1] not in labels:
                raise ValueError("Undefined label")

    # -------------------------------------------------------
    # EXECUTION HELPERS
    # -------------------------------------------------------

    def pop():
        if not stack:
            raise ValueError("Stack underflow")
        return stack.pop()

    def require(n):
        if len(stack) < n:
            raise ValueError("Stack underflow")

    # -------------------------------------------------------
    # EXECUTE
    # -------------------------------------------------------

    pc = 0
    input_pos = 0
    terminated = False

    while pc < len(instructions):
        inst = instructions[pc]
        op = inst[0]

        # ---------------- Stack ----------------

        if op == 'push':
            stack.append(inst[1])

        elif op == 'dup':
            require(1)
            stack.append(stack[-1])

        elif op == 'swap':
            require(2)
            stack[-1], stack[-2] = stack[-2], stack[-1]

        elif op == 'pop':
            pop()

        elif op == 'copy':
            n = inst[1]

            if n < 0 or n >= len(stack):
                raise ValueError("Invalid copy index")

            stack.append(stack[-1 - n])

        elif op == 'slide':
            require(1)

            n = inst[1]
            top = stack[-1]

            if n < 0 or n >= len(stack):
                stack[:] = [top]
            else:
                del stack[max(0, len(stack) - 1 - n):len(stack) - 1]

        # ---------------- Arithmetic ----------------

        elif op in ('add', 'sub', 'mul', 'div', 'mod'):
            require(2)

            a = pop()
            b = pop()

            if op == 'add':
                stack.append(b + a)

            elif op == 'sub':
                stack.append(b - a)

            elif op == 'mul':
                stack.append(b * a)

            elif op == 'div':
                if a == 0:
                    raise ValueError("Division by zero")

                # Python // already implements floor division
                stack.append(b // a)

            elif op == 'mod':
                if a == 0:
                    raise ValueError("Modulo by zero")

                # Python % has the sign of the divisor
                stack.append(b % a)

        # ---------------- Heap ----------------

        elif op == 'store':
            require(2)

            a = pop()
            b = pop()

            heap[b] = a

        elif op == 'retrieve':
            address = pop()

            if address not in heap:
                raise ValueError("Undefined heap address")

            stack.append(heap[address])

        # ---------------- Output ----------------

        elif op == 'outchar':
            value = pop()

            try:
                output.append(chr(value))
            except (ValueError, OverflowError):
                raise ValueError("Invalid character value")

        elif op == 'outnum':
            output.append(str(pop()))

        # ---------------- Input ----------------

        elif op == 'inchar':
            address = pop()

            if input_pos >= len(inp):
                raise ValueError("Input exhausted")

            heap[address] = ord(inp[input_pos])
            input_pos += 1

        elif op == 'innum':
            address = pop()

            if input_pos >= len(inp):
                raise ValueError("Input exhausted")

            end = inp.find('\n', input_pos)

            if end == -1:
                raise ValueError("Input exhausted before line-feed")

            raw = inp[input_pos:end]
            input_pos = end + 1

            try:
                # Decimal or hexadecimal (0x...)
                if raw.lower().startswith(('+0x', '-0x', '0x')):
                    value = int(raw, 16)
                else:
                    value = int(raw)
            except ValueError:
                raise ValueError("Invalid integer input")

            heap[address] = value

        # ---------------- Flow ----------------

        elif op == 'label':
            pass

        elif op == 'call':
            calls.append(pc + 1)
            pc = labels[inst[1]]
            continue

        elif op == 'jump':
            pc = labels[inst[1]]
            continue

        elif op == 'jz':
            value = pop()

            if value == 0:
                pc = labels[inst[1]]
                continue

        elif op == 'jn':
            value = pop()

            if value < 0:
                pc = labels[inst[1]]
                continue

        elif op == 'ret':
            if not calls:
                raise ValueError("Return outside subroutine")

            pc = calls.pop()
            continue

        elif op == 'end':
            terminated = True
            break

        else:
            raise ValueError("Unknown instruction")

        pc += 1

    # Program must explicitly terminate
    if not terminated:
        raise ValueError("Unclean termination")

    return ''.join(output)
