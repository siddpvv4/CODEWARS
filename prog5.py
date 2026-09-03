def to_camel_case(text):
    words = text.replace("-", "_").split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])
