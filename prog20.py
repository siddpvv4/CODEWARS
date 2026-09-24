import re
from collections import Counter

def top_3_words(text):
    words = re.findall(r"[a-zA-Z']*[a-zA-Z][a-zA-Z']*", text.lower())
    
    counts = Counter(words)
    
    return [word for word, count in counts.most_common(3)]
