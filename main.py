import axelrod as axl


def prisoner_dilemma(strategy1, strategy2, rounds=100):
    tournament = axl.Tournament([strategy1(), strategy2()], turns=rounds)
    results = tournament.play()
    score1, score2 = results.scores[0][0], results.scores[1][0]
    return score1, score2


# Example usage
score1, score2 = prisoner_dilemma(axl.TitForTat, axl.Defector)
print(f"Tit for Tat vs Always Defect: {score1} - {score2}")
