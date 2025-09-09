import nltk
from nltk.corpus import wordnet

# Download NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

def rephrase_sentence(sentence):
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)

    rephrased_sentence = []

    for word, tag in tagged:
        if tag.startswith('NN'):  # Nouns
            synsets = wordnet.synsets(word, pos=wordnet.NOUN)
            if synsets:
                rephrased_sentence.append(synsets[0].lemmas()[0].name())
            else:
                rephrased_sentence.append(word)
        elif tag.startswith('VB'):  # Verbs
            synsets = wordnet.synsets(word, pos=wordnet.VERB)
            if synsets:
                rephrased_sentence.append(synsets[0].lemmas()[0].name())
            else:
                rephrased_sentence.append(word)
        elif tag.startswith('JJ'):  # Adjectives
            synsets = wordnet.synsets(word, pos=wordnet.ADJ)
            if synsets:
                rephrased_sentence.append(synsets[0].lemmas()[0].name())
            else:
                rephrased_sentence.append(word)
        elif tag.startswith('RB'):  # Adverbs
            synsets = wordnet.synsets(word, pos=wordnet.ADV)
            if synsets:
                rephrased_sentence.append(synsets[0].lemmas()[0].name())
            else:
                rephrased_sentence.append(word)
        else:
            rephrased_sentence.append(word)

    return ' '.join(rephrased_sentence)

# Example usage
sentence = input("Enter a sentence: ")
rephrased = rephrase_sentence(sentence)
print("Rephrased sentence:", rephrased)
