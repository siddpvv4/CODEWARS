def rgb(r, g, b):
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    
    return f"{r:02X}{g:02X}{b:02X}"
