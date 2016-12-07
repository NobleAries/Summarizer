import nltk


def summarize(text, number_of_sentences):
    sentences = nltk.sent_tokenize(text)
    return '\n'.join(sentences[:number_of_sentences])
