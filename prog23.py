def fib(n):
    def fast_fib(k):
        if k == 0:
            return 0, 1

        a, b = fast_fib(k // 2)

        c = a * (2 * b - a)
        d = a * a + b * b

        if k % 2 == 0:
            return c, d
        else:
            return d, c + d

    if n >= 0:
        return fast_fib(n)[0]

    result = fast_fib(-n)[0]

    # F(-n) = (-1)^(n+1) * F(n)
    return -result if (-n) % 2 == 0 else result
