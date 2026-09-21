class RomanNumerals:

    @staticmethod
    def to_roman(n):
        values = [
            (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
            (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
            (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
        ]

        roman = ""

        for value, symbol in values:
            while n >= value:
                roman += symbol
                n -= value

        return roman

    @staticmethod
    def from_roman(roman):
        values = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000
        }

        total = 0

        for i in range(len(roman)):
            if i + 1 < len(roman) and values[roman[i]] < values[roman[i + 1]]:
                total -= values[roman[i]]
            else:
                total += values[roman[i]]

        return total
