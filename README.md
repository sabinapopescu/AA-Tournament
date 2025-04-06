# Mirror Breaker - Iterated Prisoner's Dilemma Strategy

**Author**: Popescu Sabina 
**Strategy Name**: Mirror Breaker  
**Category**: Adaptive, Exploitative, Unpredictable

---

## Overview

**Mirror Breaker** is a minimalist strategy for the Iterated Prisoner’s Dilemma.  
It begins with a cooperative stance but adapts based on the opponent's behavior—especially targeting **mirror-based strategies**, **overly kind players**, and **aggressive exploiters**.

It uses pattern detection, light probabilistic behavior, and conditional logic to **adjust mid-game tactics**.

---

## Strategy Breakdown

### Opening Behavior (Rounds 1–5)
- Starts by cooperating.
- Plays **semi-random Tit-for-Tat**, mimicking the opponent’s last move 80% of the time.
- This helps **gather intel** while remaining largely non-hostile.

### Pattern Detection (From Round 6)
- **Mirror Detection**: If the opponent mirrors your last two moves exactly, the strategy detects this and begins **reverse-mirroring** to disrupt the pattern and avoid exploitation.
- **Exploitation of Cooperators**: If the opponent has cooperated more than **80%** of the time, Mirror Breaker begins defecting occasionally (~70% chance), taking advantage of their goodwill.
- **Handling Aggressors**: If the opponent defects more than **60%**, the strategy alternates between cooperation and defection to appear unpredictable and avoid falling into punishment loops.

### General Behavior
- Adds light **randomness** in neutral cases to **resist predictability**.
- If the number of total rounds is known, it **defects in the last round** to maximize score.

---

## Why It Works

Many existing strategies rely on:
- Mirroring (Tit-for-Tat, Resettable, etc.)
- Fixed rules (Always Cooperate/Defect)
- Aggressive punishment loops

**Mirror Breaker** counters these with:
- Pattern analysis to break out of mirroring traps
- Strategic betrayal of overly generous players
- Unpredictable behavior to throw off classifiers and reactive strategies

It’s not just reactive—it’s **meta-adaptive**, designed to win by being one step ahead.

---

## Code

```python
import random

def mirror_breaker(my_history, opponent_history, rounds):
    i = len(my_history)

    if i == 0:
        return 1  # Start friendly

    if rounds and i == rounds - 1:
        return 0  # Last round = betray

    # First 6 rounds: semi-random tit-for-tat
    if i < 6:
        return opponent_history[-1] if random.random() > 0.2 else 1

    # Detect mirror-like opponent
    if my_history[-1] == opponent_history[-1] and my_history[-2] == opponent_history[-2]:
        return 0 if opponent_history[-1] else 1  # Flip to break mirror

    # Exploit too-friendly opponents
    if opponent_history.count(1) / i > 0.8:
        return 0 if random.random() > 0.3 else 1

    # Punish aggressive behavior
    if opponent_history.count(0) / i > 0.6:
        return 0 if i % 2 == 0 else 1  # Alternate to confuse

    # Otherwise, cooperate mostly with a spice of betrayal
    return 1 if random.random() > 0.15 else 0
