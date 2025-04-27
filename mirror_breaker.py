import random

def mirror_breaker(my_history, opponent_history, rounds):
    i = len(my_history)

    if i == 0:
        return 1

    if rounds and i == rounds - 1:
        return 0

    if i < 6:
        return opponent_history[-1] if random.random() > 0.2 else 1

   
    if my_history[-1] == opponent_history[-1] and my_history[-2] == opponent_history[-2]:
        return 0 if opponent_history[-1] else 1 

  
    if opponent_history.count(1) / i > 0.8:
        return 0 if random.random() > 0.3 else 1

  
    if opponent_history.count(0) / i > 0.6:
        return 0 if i % 2 == 0 else 1 

  
    return 1 if random.random() > 0.15 else 0
