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
    
# Old iterations of player classes:

# Player class has a user-inputtable target score at which point they will end their turn
# If possible, they first take a worm and generally prioritise higher dice rolls no matter the multiple
# class Player:
#     def __init__(self, name, target_score=25):
#         self.name = name
#         self.tiles = []
#         self.target_score = target_score

#     def take_turn(self):
#         current_dice = []
#         available_dice = [1, 2, 3, 4, 5, 'worm']
#         while True:
#             roll = [random.choice(available_dice) for _ in range(8 - len(current_dice))]
#             print(f"{self.name} rolls: {roll}")
            
#             # Decide which dice to keep
#             choice = self.choose_dice(roll)
#             if choice is None:
#                 break
            
#             current_dice.extend(choice)
#             print(f"{self.name} keeps: {choice} -> Current dice: {current_dice}")

#             # Check if player has reached or exceeded target score
#             total_score = self.calculate_sum(current_dice)
#             if total_score >= self.target_score and 'worm' in current_dice:
#                 break

#             if len(current_dice) == 8:  # No more dice to roll
#                 break
            
#             available_dice = [die for die in available_dice if die not in current_dice]
#             if not available_dice:  # No more dice choices left
#                 break

#         return current_dice

#     def choose_dice(self, roll):
#         counts = {die: roll.count(die) for die in set(roll)}
#         # Prioritize keeping worms if available, otherwise keep the highest value
#         if 'worm' in counts:
#             return ['worm'] * counts['worm']
#         if counts:
#             max_val = max(die for die in counts if die != 'worm')
#             return [max_val] * counts[max_val]
#         return None

#     def calculate_sum(self, kept_dice):
#         return sum(die if die != 'worm' else 5 for die in kept_dice)

#     def has_worm(self, kept_dice):
#         return 'worm' in kept_dice

#     def add_tile(self, tile):
#         self.tiles.append(tile)

#     def return_tile(self):
#         if self.tiles:
#             return self.tiles.pop()
#         return None

# # Player_Sigmoid class is similar to Player but instead of a hard cut-off at the target score has a probability to "bottle it" before the target score
# class Player_Sigmoid:
#     def __init__(self, name, target_score=25):
#         self.name = name
#         self.tiles = []
#         self.target_score = target_score

#     def sigmoid(self, x):
#         return 1 / (1 + math.exp(-x))

#     def calculate_stop_probability(self, current_score):
#         # Calculate the difference between the current score and the target score
#         difference = current_score - self.target_score
#         # Apply the sigmoid function to the difference
#         probability = self.sigmoid(difference / 5)  # Adjust the divisor to control the steepness
#         return probability

#     def take_turn(self):
#         current_dice = []
#         available_dice = [1, 2, 3, 4, 5, 'worm']
#         while True:
#             roll = [random.choice(available_dice) for _ in range(8 - len(current_dice))]
#             print(f"{self.name} rolls: {roll}")
            
#             # Decide which dice to keep
#             choice = self.choose_dice(roll)
#             if choice is None:
#                 break
            
#             current_dice.extend(choice)
#             print(f"{self.name} keeps: {choice} -> Current dice: {current_dice}")

#             # Calculate current total score
#             total_score = self.calculate_sum(current_dice)

#             # Check if player has reached or exceeded target score and decide whether to stop
#             stop_probability = self.calculate_stop_probability(total_score)
#             print(f"{self.name} has a stop probability of {stop_probability:.2f}")

#             if total_score >= 21 and 'worm' in current_dice and random.random() < stop_probability:
#                 break

#             if len(current_dice) == 8:  # No more dice to roll
#                 break
            
#             available_dice = [die for die in available_dice if die not in current_dice]
#             if not available_dice:  # No more dice choices left
#                 break

#         return current_dice

#     def choose_dice(self, roll):
#         counts = {die: roll.count(die) for die in set(roll)}
#         # Prioritize keeping worms if available, otherwise keep the highest value
#         if 'worm' in counts:
#             return ['worm'] * counts['worm']
#         if counts:
#             max_val = max(die for die in counts if die != 'worm')
#             return [max_val] * counts[max_val]
#         return None

#     def calculate_sum(self, kept_dice):
#         return sum(die if die != 'worm' else 5 for die in kept_dice)

#     def has_worm(self, kept_dice):
#         return 'worm' in kept_dice

#     def add_tile(self, tile):
#         self.tiles.append(tile)

#     def return_tile(self):
#         if self.tiles:
#             return self.tiles.pop()
#         return None

