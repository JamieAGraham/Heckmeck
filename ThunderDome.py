import random
from players import Player, CautiousPlayer, RiskTakerPlayer, BalancedPlayer, CustomPlayer
from base_v4 import Game, Tile
from collections import defaultdict

def simulate_games(num_games, num_players=4):
    # Define a mix of player types with their names
    player_type_classes = [
        ("CautiousPlayer", CautiousPlayer),
        ("RiskTakerPlayer", RiskTakerPlayer),
        ("BalancedPlayer", BalancedPlayer),
        ("CustomPlayer1", lambda name: CustomPlayer(name, risk_level=3, target_score_offset=1)),
        ("CustomPlayer2", lambda name: CustomPlayer(name, risk_level=7, target_score_offset=-1))
    ]
    
    results = defaultdict(int)
    turn_position_wins = defaultdict(int)

    for game_index in range(num_games):
        print(f"Simulating game {game_index + 1}")
        
        # Randomly select player types to ensure a mix and a total number of players less than 6
        selected_player_types = random.sample(player_type_classes, num_players)
        
        # Create unique player names
        player_counters = defaultdict(int)
        players = []
        
        for player_type_name, player_type_class in selected_player_types:
            player_counters[player_type_name] += 1
            player_name = f"{player_type_name}_{player_counters[player_type_name]}"
            players.append(player_type_class(player_name))
        
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

# Run the simulation
simulate_games(1000)