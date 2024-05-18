import random
import math
from collections import defaultdict

class Player:
    def __init__(self, name):
        self.name = name
        self.tiles = []
        self.target_score = 0

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def calculate_stop_probability(self, current_score):
        difference = current_score - self.target_score
        probability = self.sigmoid(difference / 5)
        return probability

    def take_turn(self, grill):
        available_tiles = [tile.value for tile in grill if not tile.face_down]
        if available_tiles:
            self.target_score = max(available_tiles) + random.randint(-2, 2)
        else:
            self.target_score = 21

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
    def calculate_stop_probability(self, current_score):
        difference = current_score - self.target_score
        probability = self.sigmoid(difference / 10)  # Less likely to continue
        return probability

class RiskTakerPlayer(Player):
    def calculate_stop_probability(self, current_score):
        difference = current_score - self.target_score
        probability = self.sigmoid(difference / 2)  # More likely to continue
        return probability