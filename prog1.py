def solution(number):
    if number < 0:
        return 0
    
    total_sum = 0
    for i in range(number):
        if i % 3 == 0 or i % 5 == 0:
            total_sum += i  
            
    return total_sum
i = input("Enter a number: ")
v = int(i)
result = solution(v)
print(f"The sum is: {result}")
