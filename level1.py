import random
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

random.seed(42)

passw=['AmericanPrometheus','MissionImpossible',"TheStand","TheDayOfTheJAckal"]

def similar_words(sentence, word):
    nlp = spacy.load("en_core_web_md")
    sentence_doc = nlp(sentence)
    target_word = nlp(word)
    sentence_vectors = [token.vector for token in sentence_doc]
    similarities = cosine_similarity(np.array([target_word.vector]), sentence_vectors)
    if max(similarities[0])>=0.5:
      return "I see what you did there ."
    elif 0.35<=max(similarities[0])<=0.5:
      passd=passw[random.randrange(0,len(passw))]
      return "Congratulations! The password for nxt level is:"+passd
    else:
      return sentence