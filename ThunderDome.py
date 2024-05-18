from players import Player, CautiousPlayer, RiskTakerPlayer
from base_v4 import Game, Tile
from collections import defaultdict

def simulate_games(num_games):
    player_types = [CautiousPlayer, RiskTakerPlayer]
    results = defaultdict(int)

    for _ in range(num_games):
        players = [player_type(f"Player {i + 1}") for i, player_type in enumerate(player_types * 3)]
        tiles = [Tile(value, worms) for value, worms in zip(range(21, 37), [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4])]
        game = Game(players, tiles)
        winner = game.play_game()
        results[winner.name] += 1

    for player_name, wins in results.items():
        print(f"{player_name} wins: {wins} times")

simulate_games(1000)