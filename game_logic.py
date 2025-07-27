def calculate_score(hand):
    values = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
        '7': 7, '8': 8, '9': 9, '10': 10,
        'jack': 10, 'queen': 10, 'king': 10, 'ace': 11
    }
    score = sum(values[card.split('_')[0]] for card in hand)
    num_aces = sum(1 for card in hand if card.startswith('ace'))
    
    while score > 21 and num_aces:
        score -= 10
        num_aces -= 1
    
    return score

def is_blackjack(hand):
    return calculate_score(hand) == 21 and len(hand) == 2
