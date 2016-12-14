import nltk


def summarize(text, number_of_sentences=3, outfile=None):
    sentences = nltk.sent_tokenize(text)
    summarized_text = '\n'.join(sentences[:number_of_sentences])
    if outfile is not None:
        with open(outfile, 'w') as file:
            file.write(summarized_text)
    return summarized_text
