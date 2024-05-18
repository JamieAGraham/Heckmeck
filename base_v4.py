import random
import math

class Tile:
    def __init__(self, value, worms, debug=False):
        self.value = value
        self.worms = worms
        self.face_down = False  # New attribute to indicate if the tile is face down
        self.debug = debug

    def __repr__(self):
        return f"Tile(value={self.value}, worms={self.worms}, face_down={self.face_down})"

class Player_Grill_Aware:
    def __init__(self, name, debug=False):
        self.name = name
        self.tiles = []
        self.target_score = 0
        self.debug = debug

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def calculate_stop_probability(self, current_score):
        # Calculate the difference between the current score and the target score
        difference = current_score - self.target_score
        # Apply the sigmoid function to the difference
        probability = self.sigmoid(difference / 5)  # Adjust the divisor to control the steepness
        return probability

    def take_turn(self, grill):
        # Set target score based on the highest available tile on the grill
        available_tiles = [tile.value for tile in grill if not tile.face_down]
        if available_tiles:
            self.target_score = max(available_tiles) + random.randint(-2, 2)  # Add some randomness
        else:
            self.target_score = 21  # Default to the minimum score required to claim a tile

        print(f"{self.name} sets target score to: {self.target_score}")

        current_dice = []
        available_dice = [1, 2, 3, 4, 5, 'worm']
        while True:
            roll = [random.choice(available_dice) for _ in range(8 - len(current_dice))]
            print(f"{self.name} rolls: {roll}")
            
            # Decide which dice to keep
            choice = self.choose_dice(roll)
            if choice is None:
                break
            
            current_dice.extend(choice)
            print(f"{self.name} keeps: {choice} -> Current dice: {current_dice}")

            # Calculate current total score
            total_score = self.calculate_sum(current_dice)

            # Check if player has reached or exceeded target score and decide whether to stop
            stop_probability = self.calculate_stop_probability(total_score)
            if self.debug:
                print(f"{self.name} has a stop probability of {stop_probability:.2f}")

            if total_score >= 21 and 'worm' in current_dice and random.random() < stop_probability:
                break

            if len(current_dice) == 8:  # No more dice to roll
                break
            
            available_dice = [die for die in available_dice if die not in current_dice]
            if not available_dice:  # No more dice choices left
                break

        return current_dice

    def choose_dice(self, roll):
        counts = {die: roll.count(die) for die in set(roll)}
        # Prioritize keeping worms if available, otherwise keep the highest value
        if 'worm' in counts:
            return ['worm'] * counts['worm']
        if counts:
            max_val = max(die for die in counts if die != 'worm')
            return [max_val] * counts[max_val]
        return None

    def calculate_sum(self, kept_dice):
        return sum(die if die != 'worm' else 5 for die in kept_dice)

    def has_worm(self, kept_dice):
        return 'worm' in kept_dice

    def add_tile(self, tile):
        self.tiles.append(tile)

    def return_tile(self):
        if self.tiles:
            return self.tiles.pop()
        return None



class Game:
    def __init__(self, players, tiles, debug=False):
        self.players = players
        self.center_tiles = tiles
        self.debug = debug

    def play_turn(self, player):
        kept_dice = player.take_turn(self.center_tiles)
        if not self.claim_tile(player, kept_dice) and self.debug:
            print(f"{player.name} failed to claim a tile and returned one to the center.")
        
        # Check if all center tiles are face down
        if all(tile.face_down for tile in self.center_tiles):
            if self.debug:
                print("All tiles are face down. Game over.")
            return False  # Indicate the game should end
        return True  # Indicate the game should continue

    def play_game(self):
        turn_counter = 0
        while turn_counter < 1000:  # Cap to avoid infinite loops in testing
            for player in self.players:
                turn_counter += 1
                if self.debug:
                    print(f"Turn {turn_counter}")
                if not self.play_turn(player):
                    if self.debug:
                        self.print_final_scores()
                    return self.calculate_winner() # End the game

                # Debug: Print remaining center tiles
                remaining_tiles = [tile for tile in self.center_tiles if not tile.face_down]
                if self.debug:
                    print(f"Remaining center tiles: {[tile.value for tile in remaining_tiles]}")

        print("Reached maximum number of turns. Game over.")
        self.print_final_scores()

    def claim_tile(self, player, kept_dice):
        total = player.calculate_sum(kept_dice)
        if self.debug:
            print(f"{player.name} tries to claim with total: {total} and dice: {kept_dice}")
        
        if total >= 21 and player.has_worm(kept_dice):
            available_tiles = [tile for tile in self.center_tiles if tile.value <= total and not tile.face_down]
            if self.debug:
                print(f"Available tiles: {[tile.value for tile in available_tiles]}")
            
            if available_tiles:
                claimed_tile = max(available_tiles, key=lambda t: t.value)
                player.add_tile(claimed_tile)
                self.center_tiles.remove(claimed_tile)
                if self.debug:
                    print(f"{player.name} claims tile: {claimed_tile.value} -> Tiles: {player.tiles}")
                return True  # Successful claim
            else:
                # Check if the player can steal a tile from another player
                for other_player in self.players:
                    if other_player != player and other_player.tiles and other_player.tiles[-1].value == total:
                        player.add_tile(other_player.tiles.pop())
                        if self.debug:
                            print(f"{player.name} steals tile from {other_player.name} -> Tiles: {player.tiles}")
                        return True  # Successful claim
        
        returned_tile = player.return_tile()
        if returned_tile:
            self.center_tiles.append(returned_tile)
            self.center_tiles = sorted(self.center_tiles, key=lambda t: t.value)
            if self.debug:
                print(f"{player.name} fails and returns tile: {returned_tile.value} -> Center tiles: {[tile.value for tile in self.center_tiles if not tile.face_down]}")

            # Turn the highest available tile face down
            non_face_down_tiles = [tile for tile in self.center_tiles if not tile.face_down]
            if non_face_down_tiles:
                highest_tile = max(non_face_down_tiles, key=lambda t: t.value)
                highest_tile.face_down = True
                if self.debug:
                    print(f"The highest tile {highest_tile.value} is now face down.")
        
        return False  # Failed claim
    
    def calculate_winner(self):
        scores = {player: sum(tile.worms for tile in player.tiles) for player in self.players}
        max_score = max(scores.values())
        candidates = [player for player, score in scores.items() if score == max_score]
        if len(candidates) == 1:
            winner = candidates[0]
        else:
            winner = max(candidates, key=lambda p: max(tile.value for tile in p.tiles))
        winner_position = self.players.index(winner)
        return winner, winner_position


    def print_final_scores(self):
        print("Final Scores:")
        scores = {}
        for player in self.players:
            score = sum(tile.worms for tile in player.tiles)
            scores[player] = score
            print(f"{player.name}: {score} worms")

        # Determine the winner
        max_score = max(scores.values())
        candidates = [player for player, score in scores.items() if score == max_score]

        if len(candidates) == 1:
            winner = candidates[0]
        else:
            # Tie-breaking logic based on the most valuable single worm helping
            winner = max(candidates, key=lambda p: max(tile.value for tile in p.tiles))

        print(f"The winner is {winner.name} with {scores[winner]} worms.")

# Create game instance
players = [
    Player_Grill_Aware("Player A"),
    Player_Grill_Aware("Player B"),
    Player_Grill_Aware("Player C"),
    Player_Grill_Aware("Player D"),
    Player_Grill_Aware("Player E"),
    Player_Grill_Aware("Player F")
]

# Create tiles
tiles = [Tile(value, worms) for value, worms in zip(range(21, 37), [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4])]

# Create game instance
game = Game(players, tiles)

# Run the game
game.play_game()