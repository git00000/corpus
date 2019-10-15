import string

def word_count(text):
    """
    return the word count in a string
    """
    
    for punc in string.punctuation:
        text = text.replace(punc, '')
    words = text.split()
    word_count = len(words)
    return word_count
