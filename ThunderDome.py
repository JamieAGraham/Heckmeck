import random
from players import Player, CautiousPlayer, RiskTakerPlayer, BalancedPlayer, CustomPlayer
from base_v4 import Game, Tile
from collections import defaultdict

def simulate_game(player1, player2):
    tiles = [Tile(value, worms) for value, worms in zip(range(21, 37), [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4])]
    game = Game([player1, player2], tiles)
    
    # Reset players' tiles before starting the game
    player1.reset()
    player2.reset()

    winner, _ = game.play_game()
    return winner.name

def round_robin(players, num_games):
    num_players = len(players)
    results = [[0 for _ in range(num_players)] for _ in range(num_players)]
    matchups = [(i, j) for i in range(num_players) for j in range(i + 1, num_players)]
    
    for i, j in matchups:
        player1 = players[i]
        player2 = players[j]
        for _ in range(num_games):
            winner = simulate_game(player1, player2)
            if winner == player1.name:
                results[i][j] += 1
            else:
                results[j][i] += 1
            
            # Alternate the starting player
            winner = simulate_game(player2, player1)
            if winner == player2.name:
                results[j][i] += 1
            else:
                results[i][j] += 1

    return results

def simulate_tournament():
    player_type_classes = [
        ("CautiousPlayer", CautiousPlayer),
        ("RiskTakerPlayer", RiskTakerPlayer),
        ("BalancedPlayer", BalancedPlayer),
        ("CustomPlayer1", lambda name: CustomPlayer(name, risk_level=3, target_score_offset=1)),
        ("CustomPlayer2", lambda name: CustomPlayer(name, risk_level=7, target_score_offset=-1)),
        ("CustomPlayer5", lambda name: CustomPlayer(name, risk_level=2, target_score_offset=5)),
        ("CustomPlayer7", lambda name: CustomPlayer(name, risk_level=2, target_score_offset=7))
    ]
    
    players = [player_type_class(f"{player_type_name}_{i + 1}")
               for player_type_name, player_type_class in player_type_classes
               for i in range(1)]
    
    num_games = 9794  # Reduced for quicker test runs
    results = round_robin(players, num_games)
    
    # Print results in grid format with explicit axis labeling
    print("Results Grid (Number of Wins):")
    player_names = [player.name for player in players]
    
    # Print header row
    header = "\t".join([""] + player_names)
    print(header)
    
    # Print each row
    for i, player_name in enumerate(player_names):
        row = [player_name] + results[i]
        print("\t".join(map(str, row)))
    
    print("\nDetailed Matchups (Wins for each player against every other player):")
    for i, player_name_1 in enumerate(player_names):
        for j, player_name_2 in enumerate(player_names):
            if i != j:
                print(f"{player_name_1} vs {player_name_2}: {results[i][j]} wins")

# Run the tournament simulation
simulate_tournament()