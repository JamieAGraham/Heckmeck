import random
import math

class Player:
    def __init__(self, name, risk_level=5, target_score_offset=0):
        self.name = name
        self.tiles = []
        self.target_score = 0
        self.risk_level = risk_level
        self.target_score_offset = target_score_offset

        
    def reset(self):
        # Added when looping as existing players did not reset tiles when playing multiple games.
        # This should *probably* be run at the end of each game but in the ThunderDome loop this has been done explicitly
        # when starting each match up in the round robin.
        self.tiles = []

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def calculate_stop_probability(self, current_score):
        difference = current_score - self.target_score
        probability = self.sigmoid(difference / self.risk_level)
        return probability

    def take_turn(self, grill):
        available_tiles = [tile.value for tile in grill if not tile.face_down]
        if available_tiles:
            self.target_score = max(available_tiles) + self.target_score_offset
        else:
            self.target_score = 21 + self.target_score_offset

        current_dice = []
        available_dice = [1, 2, 3, 4, 5, 'worm']
        while True:
            roll = [random.choice(available_dice) for _ in range(8 - len(current_dice))]
            choice = self.choose_dice(roll)
            if choice is None:
                break
            
            current_dice.extend(choice)
            total_score = self.calculate_sum(current_dice)

            stop_probability = self.calculate_stop_probability(total_score)
            if total_score >= 21 and 'worm' in current_dice and random.random() < stop_probability:
                break

            if len(current_dice) == 8:
                break
            
            available_dice = [die for die in available_dice if die not in current_dice]
            if not available_dice:
                break

        return current_dice

    def choose_dice(self, roll):
        counts = {die: roll.count(die) for die in set(roll)}
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

class CautiousPlayer(Player):
    def __init__(self, name):
        super().__init__(name, risk_level=10, target_score_offset=-2)

class RiskTakerPlayer(Player):
    def __init__(self, name):
        super().__init__(name, risk_level=2, target_score_offset=2)

class BalancedPlayer(Player):
    def __init__(self, name):
        super().__init__(name, risk_level=5, target_score_offset=0)

class CustomPlayer(Player):
    def __init__(self, name, risk_level, target_score_offset):
        super().__init__(name, risk_level, target_score_offset)
    

class AdaptivePlayer(Player):
    def __init__(self, name, initial_risk_level=5, risk_reduction_factor=0.5, target_score_offset=0):
        super().__init__(name)
        self.initial_risk_level = initial_risk_level
        self.risk_reduction_factor = risk_reduction_factor
        self.target_score_offset = target_score_offset

    def calculate_lead(self, players):
        my_score = sum(tile.worms for tile in self.tiles)
        scores = [sum(tile.worms for tile in player.tiles) for player in players if player != self]
        max_opponent_score = max(scores, default=0)
        return my_score - max_opponent_score

    def should_roll_again(self, current_score, center_tiles, players):
        lead = self.calculate_lead(players)
        dynamic_risk_level = max(self.initial_risk_level - (lead * self.risk_reduction_factor), 1)  # Ensure risk level doesn't drop below 1
        target_score = 20 + self.target_score_offset
        return random.random() < 1 / (1 + math.exp(-(current_score - target_score) / dynamic_risk_level))

