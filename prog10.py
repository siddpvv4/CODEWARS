def digital_root(n):
    while n >= 10:
        total = 0
        
        for digit in str(n):
            total += int(digit)
        
        n = total
    
    return n
