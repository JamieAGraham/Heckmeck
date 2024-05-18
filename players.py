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
            max_val = max(d for d in dice_roll if d != 'worm')
            return [d for d in dice_roll if d == max_val]
        elif self.strategy == "balanced":
            if 'worm' in dice_roll:
                return [d for d in dice_roll if d == 'worm']
            else:
                max_val = max(dice_roll)
                return [d for d in dice_roll if d == max_val]

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