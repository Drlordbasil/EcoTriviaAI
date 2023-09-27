```python
import os
import random
from typing import List, Union
class TriviaQuestion:
    def __init__(self, fact: str, answer: Union[str, bool] = None):
        self.fact = fact
        self.answer = answer if answer else "?"
        
def get_ecotrivia_question(topic: str) -> TriviaQuestion:
    with open("data/openai-gpt4.json", "r") as f:
        model_url = f.read().strip()
    
    response = requests.get(model_url + "/generate/trivia?topics=" + topic).text
    questions = [q for q in (s.split(":"))[1].split("\n") if s.startswith("Q:")]
    random.shuffle(questions)
    
    question = questions[-1]
    answer = None
    
    if "Yes" in response or "True" in response:
        answer = True
    elif "-" in response:
        pass
    else:
        answer = False
        
    return TriviaQuestion(question.replace("Q:", ""), answer=answer)
def play_ecotrivia():
    while True:
        print("\nEcoTrivia AI\n")
        topic = input("Enter a trivia topic (environment, conservation, etc.): ")
        
        if not os.path.exists("