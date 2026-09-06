import math

def is_prime(num):
    # Prime numbers must be greater than 1
    if num <= 1:
        return False
    
    # 2 is the only even prime number
    if num == 2:
        return True
    
    # Exclude all other even numbers immediately
    if num % 2 == 0:
        return False
    
    # Check odd factors up to the square root of num
    limit = int(math.isqrt(num))
    for i in range(3, limit + 1, 2):
        if num % i == 0:
            return False
            
    return True
