from CharacterType import CharacterType
from Deck import Deck


class Player:
    def __init__(self, cards: Deck = None, limit: int = None, character: CharacterType = None):
        self.cards = cards or Deck()
        self.limit = limit
        self.life = 10
        self.character = character
        self.points = 0
        self.died_turn = 0
