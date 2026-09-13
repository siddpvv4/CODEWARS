def find_nb(m):
    total = 0
    n = 0
    
    while total < m:
        n += 1
        total += n ** 3
    
    if total == m:
        return n
    return -1
