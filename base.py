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
            if 'worm' in dice_roll and all(d == 'worm' for d in self.current_dice):
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
            max_tile_value = max((tile.value for tile in self.tiles), default=0)
            candidate_values = [d for d in dice_roll if d != 'worm' and d >= max_tile_value]
            if candidate_values:
                choice = max(candidate_values)
                return [d for d in dice_roll if d == choice]
            else:
                if 'worm' in dice_roll:
                    return [d for d in dice_roll if d == 'worm']
                else:
                    return [d for d in dice_roll if d == random.choice(dice_roll)]

    def add_tile(self, tile):
        self.tiles.append(tile)
        self.score += tile.worms

    def return_tile(self):
        if self.tiles:
            return self.tiles.pop()
        return None

    def calculate_sum(self, kept_dice):
        return sum(d for d in kept_dice if d != 'worm') + 5 * kept_dice.count('worm')

    def has_worm(self, kept_dice):
        return 'worm' in kept_dice
    

class Tile:
    def __init__(self, value, worms):
        self.value = value
        self.worms = worms

    def __repr__(self):
        return f"Tile(value={self.value}, worms={self.worms})"

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
            choice = player.choose_dice(dice_roll)
            if not choice:
                break
            player.current_dice.extend(choice)
            dice_count -= len(choice)
            if len(set(choice)) == 1 and choice[0] == 'worm':
                break
        return player.current_dice

    def claim_tile(self, player, kept_dice):
        total = player.calculate_sum(kept_dice)
        if total >= 21 and player.has_worm(kept_dice):
            available_tiles = [tile for tile in self.center_tiles if tile.value <= total]
            if available_tiles:
                claimed_tile = max(available_tiles, key=lambda t: t.value)
                player.add_tile(claimed_tile)
                self.center_tiles.remove(claimed_tile)
                return
            for other_player in self.players:
                if other_player != player and other_player.tiles and other_player.tiles[-1].value == total:
                    player.add_tile(other_player.tiles.pop())
                    return
        returned_tile = player.return_tile()
        if returned_tile:
            self.center_tiles.append(returned_tile)
            self.center_tiles = sorted(self.center_tiles, key=lambda t: t.value)
            self.center_tiles[-1].value *= -1  # Flip the highest tile

    def play_game(self):
        while self.center_tiles:
            for player in self.players:
                kept_dice = self.play_turn(player)
                self.claim_tile(player, kept_dice)
        
        for player in self.players:
            print(f"{player.name}'s tiles: {player.tiles} with score: {player.score}")

        winner = max(self.players, key=lambda p: p.score)
        print(f"The winner is {winner.name} with {winner.score} worms!")

# Example setup with multiple strategies
players = [
    Player("Player 1", "random"),
    Player("Player 2", "greedy"),
    Player("Player 3", "balanced"),
    Player("Player 4", "cautious"),
    Player("Player 5", "aggressive"),
    Player("Player 6", "opportunistic")
]

game = Game(players)
game.play_game()