import random


class Player:
    def __init__(self, name, strategy):
        self.name = name
        self.tiles = []
        self.strategy = strategy
        self.current_dice = []
        self.score = 0

    def roll_dice(self, dice_count):
        return [random.choice([1, 2, 3, 4, 5, 'worm']) for _ in range(dice_count)]

    def choose_dice(self, dice_roll):
        if self.strategy == "random":
            return [d for d in dice_roll if d == random.choice(dice_roll)]
        elif self.strategy == "greedy":
            non_worms = [d for d in dice_roll if d != 'worm']
            if non_worms:
                max_val = max(non_worms)
                return [d for d in dice_roll if d == max_val]
            else:
                return [d for d in dice_roll if d == 'worm']
        elif self.strategy == "balanced":
            if 'worm' in dice_roll and not any(d == 'worm' for d in self.current_dice):
                return [d for d in dice_roll if d == 'worm']
            else:
                non_worms = [d for d in dice_roll if d != 'worm']
                if non_worms:
                    max_val = max(non_worms)
                    return [d for d in dice_roll if d == max_val]
                else:
                    return [d for d in dice_roll if d == 'worm']
        elif self.strategy == "cautious":
            if 'worm' in dice_roll:
                return [d for d in dice_roll if d == 'worm']
            else:
                min_val = min(dice_roll)
                return [d for d in dice_roll if d == min_val]
        elif self.strategy == "aggressive":
            if 'worm' in dice_roll and not self.current_dice:
                return [d for d in dice_roll if d == 'worm']
            else:
                non_worms = [d for d in dice_roll if d != 'worm']
                if non_worms:
                    max_val = max(non_worms)
                    return [d for d in dice_roll if d == max_val]
                else:
                    return [d for d in dice_roll if d == 'worm']
        elif self.strategy == "opportunistic":
            max_tile_value = max(tile.value for tile in self.tiles) if self.tiles else 0
            candidate_values = [d for d in dice_roll if d != 'worm' and d >= max_tile_value]
            if candidate_values:
                choice = max(candidate_values)
                return [d for d in dice_roll if d == choice]
            else:
                return [d for d in dice_roll if d == 'worm'] if 'worm' in dice_roll else [d for d in dice_roll if d == random.choice(dice_roll)]

    def add_tile(self, tile):
        self.tiles.append(tile)
        self.update_score()

    def return_tile(self):
        if self.tiles:
            return self.tiles.pop()
        return None

    def calculate_sum(self, kept_dice):
        # Count the number of worms and calculate the sum of non-worm dice
        non_worm_sum = sum(d for d in kept_dice if d != 'worm')
        worm_count = kept_dice.count('worm')

        # Calculate the total sum including worms
        total = non_worm_sum + 5 * worm_count
        return total

    def has_worm(self, kept_dice):
        return 'worm' in kept_dice

    def update_score(self):
        self.score = sum(tile.worms for tile in self.tiles)
    

class Tile:
    def __init__(self, value, worms):
        self.value = value
        self.worms = worms
        self.face_down = False  # New attribute to indicate if the tile is face down

    def __repr__(self):
        return f"Tile(value={self.value}, worms={self.worms}, face_down={self.face_down})"


class Game:
    def __init__(self, players):
        self.players = players
        self.tiles = [Tile(value, (value - 20) // 4) for value in range(21, 37)]
        random.shuffle(self.tiles)
        self.center_tiles = self.tiles[:]

    def play_turn(self, player):
        dice_count = 8
        player.current_dice = []
        while dice_count > 0:
            dice_roll = player.roll_dice(dice_count)
            print(f"{player.name} rolls: {dice_roll}")
            choice = player.choose_dice(dice_roll)
            if not choice:
                break
            player.current_dice.extend(choice)
            dice_count -= len(choice)
            print(f"{player.name} keeps: {choice} -> Current dice: {player.current_dice}")
            if len(set(choice)) == 1 and choice[0] == 'worm':
                break
        return player.current_dice

    def claim_tile(self, player, kept_dice):
        total = player.calculate_sum(kept_dice)
        print(f"{player.name} tries to claim with total: {total} and dice: {kept_dice}")
        
        if total >= 21 and player.has_worm(kept_dice):
            available_tiles = [tile for tile in self.center_tiles if tile.value <= total and not tile.face_down]
            print(f"Available tiles: {[tile.value for tile in available_tiles]}")
            
            if available_tiles:
                claimed_tile = max(available_tiles, key=lambda t: t.value)
                player.add_tile(claimed_tile)
                self.center_tiles.remove(claimed_tile)
                print(f"{player.name} claims tile: {claimed_tile.value} -> Tiles: {player.tiles}")
                return True  # Successful claim
            else:
                # Check if the player can steal a tile from another player
                for other_player in self.players:
                    if other_player != player and other_player.tiles and other_player.tiles[-1].value == total:
                        player.add_tile(other_player.tiles.pop())
                        print(f"{player.name} steals tile from {other_player.name} -> Tiles: {player.tiles}")
                        return True  # Successful claim
        
        returned_tile = player.return_tile()
        if returned_tile:
            self.center_tiles.append(returned_tile)
            self.center_tiles = sorted(self.center_tiles, key=lambda t: t.value)
            print(f"{player.name} fails and returns tile: {returned_tile.value} -> Center tiles: {[tile.value for tile in self.center_tiles if not tile.face_down]}")

            # Turn the highest available tile face down
            non_face_down_tiles = [tile for tile in self.center_tiles if not tile.face_down]
            if non_face_down_tiles:
                highest_tile = max(non_face_down_tiles, key=lambda t: t.value)
                highest_tile.face_down = True
                print(f"The highest tile {highest_tile.value} is now face down.")
        
        return False  # Failed claim


    def play_game(self):
        turn_counter = 0
        while self.center_tiles:
            turn_counter += 1
            for player in self.players:
                kept_dice = self.play_turn(player)
                success = self.claim_tile(player, kept_dice)
                if not success:
                    print(f"{player.name} failed to claim a tile and returned one to the center.")

            # Debugging output to check the state of center tiles and turn counter
            print(f"Turn {turn_counter}: Remaining center tiles - {[tile.value for tile in self.center_tiles]}")

            # If turn count exceeds a reasonable threshold, break to avoid infinite loop
            if turn_counter > 1000:
                print("Game terminated early due to excessive turns.")
                break

        for player in self.players:
            print(f"{player.name}'s tiles: {player.tiles} with score: {player.score}")

        winner = max(self.players, key=lambda p: p.score)
        print(f"The winner is {winner.name} with {winner.score} worms!")
        print(f"Total turns taken: {turn_counter}")

# Example setup with multiple strategies
players = [
    Player("Player 1", "random"),
    Player("Player 2", "greedy"),
    Player("Player 3", "random"),
    Player("Player 4", "random"),
    Player("Player 5", "greedy"),
    Player("Player 6", "greedy")
]

game = Game(players)
game.play_game()