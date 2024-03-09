import random
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import google.generativeai as genai


def similar_words(sentence, word, password):
    nlp = spacy.load("en_core_web_md")
    sentence_doc = nlp(sentence)
    target_word = nlp(word)
    sentence_vectors = [token.vector for token in sentence_doc]
    similarities = cosine_similarity(np.array([target_word.vector]), sentence_vectors)
    if max(similarities[0]) >= 0.95:
      return "The password is: " + word
    else :
      return "Similarity Score :"+str(similarities[0][0])
    
def getHint(password,apiKey):
  genai.configure(api_key=apiKey)
  safety_settings = [
      {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
      },
      {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
      },
      {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
      },
      {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
      },
    ]
  model = genai.GenerativeModel(model_name="gemini-pro",
                                  safety_settings=safety_settings)
  hint=model.generate_content(f"Give a complex hint related to the word {password} without mentioning it.")
  return hint.text