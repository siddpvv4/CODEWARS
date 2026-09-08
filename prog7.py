def sum_digits(num_str):
    return sum(int(digit) for digit in num_str)

def order_weight(strng):
    
    numbers = strng.split()
    if not numbers:
        return ""
    
   
    sorted_numbers = sorted(numbers, key=lambda x: (sum_digits(x), x))
    
    return " ".join(sorted_numbers)
