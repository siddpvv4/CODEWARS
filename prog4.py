def create_phone_number(n):
    template = "(xxx) xxx-xxxx"
    for digit in n:
        template = template.replace('x', str(digit), 1)
    return template
