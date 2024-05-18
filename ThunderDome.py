import random
from players import Player, CautiousPlayer, RiskTakerPlayer, BalancedPlayer, CustomPlayer
from base_v4 import Game, Tile
from collections import defaultdict

def simulate_game(player1, player2):
    player1.reset()
    player2.reset()
    tiles = [Tile(value, worms) for value, worms in zip(range(21, 37), [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4])]
    game = Game([player1, player2], tiles, debug=True)
    winner, _ = game.play_game()
    return winner.name

def round_robin(players, num_games):
    results = defaultdict(int)
    matchups = [(i, j) for i in range(len(players)) for j in range(i + 1, len(players))]
    
    for i, j in matchups:
        player1 = players[i]
        player2 = players[j]
        for _ in range(num_games):
            winner = simulate_game(player1, player2)
            results[winner] += 1
            
            # Alternate the starting player
            winner = simulate_game(player2, player1)
            results[winner] += 1

    return results

def simulate_tournament():
    player_type_classes = [
        ("CautiousPlayer", CautiousPlayer),
        ("RiskTakerPlayer", RiskTakerPlayer),
        ("BalancedPlayer", BalancedPlayer),
        ("CustomPlayer1", lambda name: CustomPlayer(name, risk_level=3, target_score_offset=1)),
        ("CustomPlayer2", lambda name: CustomPlayer(name, risk_level=7, target_score_offset=-1))
    ]
    
    players = [player_type_class(f"{player_type_name}_{i + 1}")
               for player_type_name, player_type_class in player_type_classes
               for i in range(1)]
    
    num_games = 9794  # Sample size for detecting a 2% effect size
    results = round_robin(players, num_games)
    
    for player_name, wins in results.items():
        print(f"{player_name} wins: {wins} times")

# Run the tournament simulation
simulate_tournament()