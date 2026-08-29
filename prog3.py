def find_short(s):
    words = s.split()
    sh = len(words[0])
    for i in words:
        if len(i) < sh:
            sh = len(i)
    return sh
