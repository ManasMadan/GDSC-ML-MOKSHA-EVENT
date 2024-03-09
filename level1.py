import random
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def similar_words(sentence, word, password):
    nlp = spacy.load("en_core_web_md")
    sentence_doc = nlp(sentence)
    target_word = nlp(word)
    sentence_vectors = [token.vector for token in sentence_doc]
    similarities = cosine_similarity(np.array([target_word.vector]), sentence_vectors)
    if max(similarities[0])>=0.5:
      return "I see what you did there."
    elif 0.35<=max(similarities[0])<=0.5:
      selected_password = password
      return "Congratulations! The password for next level is " + selected_password
    else:
      return sentence