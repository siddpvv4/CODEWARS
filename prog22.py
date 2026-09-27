def is_interesting(number, awesome_phrases):
    
    def check(n):
        if n < 100:
            return False
        
        s = str(n)

        # Any digit followed by all zeros
        if s[1:] == "0" * (len(s) - 1):
            return True

        # All digits are the same
        if len(set(s)) == 1:
            return True

        # Sequential incrementing
        if s in "1234567890":
            return True

        # Sequential decrementing
        if s in "9876543210":
            return True

        # Palindrome
        if s == s[::-1]:
            return True

        # Awesome phrase
        if n in awesome_phrases:
            return True

        return False

    # Interesting right now
    if check(number):
        return 2

    # Interesting within next 2 miles
    if check(number + 1) or check(number + 2):
        return 1

    return 0
