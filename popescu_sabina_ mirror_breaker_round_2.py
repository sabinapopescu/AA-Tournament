def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    def decide_move(my_hist, opp_hist):
        i = len(my_hist)

        if i == 0:
            return 1 

        if i >= 199:
            return 0

        if i >= 2 and my_hist[-1] == opp_hist[-1] and my_hist[-2] == opp_hist[-2]:
            return 0 if opp_hist[-1] else 1

        coop_ratio = opp_hist.count(1) / i if i > 0 else 0

        if coop_ratio > 0.8:
            return 0

        deflect_ratio = opp_hist.count(0) / i if i > 0 else 0

        if deflect_ratio > 0.6:
            return 0 if i % 2 == 0 else 1

        return 1 if (i % 7 != 0) else 0

    def select_opponent(my_hist, opp_hist):
        candidates = [pid for pid in my_hist if len(my_hist[pid]) < 200]

        if not candidates:
            return opponent_id
        best_score = -1
        best_opponent = candidates[0]

        for pid in candidates:
            opp_moves = opp_hist.get(pid, [])
            total_moves = len(opp_moves)
            if total_moves == 0:
                score = 1
            else:
                coop_ratio = opp_moves.count(1) / total_moves
                score = coop_ratio - (total_moves / 200)

            if score > best_score:
                best_score = score
                best_opponent = pid

        return best_opponent

    move = decide_move(my_history.get(opponent_id, []), opponents_history.get(opponent_id, []))
    next_opponent = select_opponent(my_history, opponents_history)

    return move, next_opponent
