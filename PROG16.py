import re
def increment_string(strng):
    match = re.search(r'(\d+)$', strng)
    if match:
        number_str = match.group(1)
        length = len(number_str)
        incremented_number = str(int(number_str) + 1).zfill(length)
        return strng[:-length] + incremented_number
    
    
    return strng + '1'
