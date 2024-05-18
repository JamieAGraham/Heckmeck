from players import Player, CautiousPlayer, RiskTakerPlayer
from base_v4 import Game, Tile
from collections import defaultdict

def simulate_games(num_games):
    player_types = [CautiousPlayer, RiskTakerPlayer]
    results = defaultdict(int)
    turn_position_wins = defaultdict(int)

    for game_index in range(num_games):
        print(f"Simulating game {game_index + 1}")
        players = [player_type(f"Player {i + 1}") for i, player_type in enumerate(player_types * 3)]
        tiles = [Tile(value, worms) for value, worms in zip(range(21, 37), [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4])]
        game = Game(players, tiles)
        winner, winner_position = game.play_game()
        results[winner.name] += 1
        turn_position_wins[winner_position] += 1

    for player_name, wins in results.items():
        print(f"{player_name} wins: {wins} times")

    print("\nWinner Position Distribution:")
    for position, wins in turn_position_wins.items():
        print(f"Turn position {position + 1}: {wins} wins")

simulate_games(1000)