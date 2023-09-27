import requests
from bs4 import BeautifulSoup
import nltk
import json
import random
import openai

nltk.download("wordnet")
from wordnet import synset, prenom_scores

# Initialize OpenAI GPT-4 model
tokenizer = openai.pt.PiecewiseConstantTokenizer(openai.pt.PRETRAINED)
model = openai.pt.PretrainedModel.from_pretrained(
    "GPT-4", tokenizer=tokenizer, device="cpu"
)


# Function to get eco-themed trivia question using OpenAI GPT-4 model
def get_ecotrivia_question(self, topic):
    # Fetch relevant Wikipedia page using BeautifulSoup
    response = requests.get("https://en.wikipedia.org/wiki/{0}".format(topic))
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract important sentences from the article
    important_sentences = []
    for sentence in soup.find_all("span", {"class": "FirstHeading"}):
        important_sentences.append((sentence.get_text(), response.url))

    # Pass extracted text to OpenAI GPT-4 model and generate a question
    context = " ".join(
        [
            word
            for word, _ in openai.pt.PiecewiseConstantTokenizer(openai.pt.PRETRAINED)[
                "gutenberg/words"
            ]()
        ]
    )

    # Use WordNet to find synonyms with high prestige scores
    synsets = []
    for synset in synset.synsets():
        if topic in synset.lemmas():
            score = sum(prenom_scores[lemma._word] for lemma in synset.lemmas())

        # Filter out low-score synonyms to maintain question quality
        if score >= 20:
            synsets.append((synset, score))
    if not synsets:
        continue

    best_synset = max(synsets, key=lambda x: x[1])
    wordnet_lemma = best_synset[0]
    prestige_score = best_synset[1]

    question = "What is {word}?".format(
        word=nltk.tokenize.word_tokenize(sentence.get_text())[-1]
    )
