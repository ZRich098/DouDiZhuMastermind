colors = ['hearts', 'diamonds', 'spades', 'clubs', 'joker']

class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

    def __repr__ (self):
        table = {
            11: "Jack",
            12: "Queen",
            13: "King",
            14: "Ace",
            15: "Two"}

        if self.value == 16: return "Uncolored Joker"
        elif self.value == 17: return "Colored Joker"
        return table.get(self.value,str(self.value)) + " of " + self.color
