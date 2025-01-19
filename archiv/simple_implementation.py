import random


def prisoner_dilemma(strategy1, strategy2, rounds=100):
    payoff_matrix = {
        ('cooperate', 'cooperate'): (3, 3),
        ('cooperate', 'defect'): (0, 5),
        ('defect', 'cooperate'): (5, 0),
        ('defect', 'defect'): (1, 1)
    }

    score1, score2 = 0, 0
    history1, history2 = [], []

    for _ in range(rounds):
        choice1 = strategy1(history1, history2)
        choice2 = strategy2(history2, history1)
        history1.append(choice1)
        history2.append(choice2)
        payoff1, payoff2 = payoff_matrix[(choice1, choice2)]
        score1 += payoff1
        score2 += payoff2

    return score1, score2


def always_cooperate(_, __):
    return 'cooperate'


def always_defect(_, __):
    return 'defect'


def tit_for_tat(history1, history2):
    if not history2:
        return 'cooperate'
    return history2[-1]


def random_strategy(_, __):
    return random.choice(['cooperate', 'defect'])


# Example usage
score1, score2 = prisoner_dilemma(tit_for_tat, always_defect)
print(f"Tit for Tat vs Always Defect: {score1} - {score2}")
