
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
```

---

## Second Round - Multi-Opponent Logic

Mirror Breaker is also designed for tournaments involving **multiple opponents** where it must **choose the next opponent** after each move.  

Key Points:
- Always cooperate first move.
- Always betray last move against an opponent.
- Detect mirror-like behavior and break it.
- Exploit cooperators (>80% cooperation rate).
- Punish defectors (<40% cooperation rate) by alternating moves.
- Prefer playing against the most cooperative opponents.

### Second Round Code

```python
def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    MAX_ROUNDS = 200  # Max rounds per opponent

    # Decide Move
    my_moves = my_history.get(opponent_id, [])
    opp_moves = opponents_history.get(opponent_id, [])
    rounds = len(my_moves)

    if rounds == 0:
        move = 1  # Always start cooperating

    elif rounds == MAX_ROUNDS - 1:
        move = 0  # Last chance, stab them in the back

    elif rounds < 6:
        move = opp_moves[-1] if opp_moves else 1  # Copy last move if exists, else cooperate

    elif len(my_moves) >= 2 and my_moves[-1] == opp_moves[-1] and my_moves[-2] == opp_moves[-2]:
        move = 0 if opp_moves[-1] else 1  # Break mirrors

    else:
        coop_rate = sum(opp_moves) / rounds if rounds else 1

        if coop_rate > 0.8:
            move = 0  # They are too nice, betray

        elif coop_rate < 0.4:
            move = 0 if rounds % 2 == 0 else 1  # Punish bullies with confusing pattern

        else:
            move = 1  # Mostly cooperate

    # Decide Next Opponent
    available_opponents = [pid for pid, moves in my_history.items() if len(moves) < MAX_ROUNDS]
    if opponent_id not in available_opponents and len(my_moves) < MAX_ROUNDS:
        available_opponents.append(opponent_id)

    if not available_opponents:
        next_opponent = opponent_id  # No choice

    else:
        # Prefer opponents with highest cooperation rate
        best_score = -1
        next_opponent = opponent_id  # fallback

        for pid in available_opponents:
            opp_hist = opponents_history.get(pid, [])
            if not opp_hist:
                score = 1  # Assume good if unknown
            else:
                score = sum(opp_hist) / len(opp_hist)

            if score > best_score:
                best_score = score
                next_opponent = pid

    return move, next_opponent
```

---


#  Final Words

Mirror Breaker isn't built to look good. It's built to **win** — through adaptability, pattern disruption, and subtle exploitation.  
Test it. Break it. Tune it. That's how you create a real tournament-ready strategy.

