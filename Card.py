from CardType import CardType
from CardValue import CardValue
import random

class Card:
    def __init__(self, value: CardValue):
        self.value = value
        self.type = CardType.get_type(value)

    def effect(self, player, discarded_deck):
        if self.value == CardValue.TSUNAMI or self.value == CardValue.HURRICAN:
            if player.cards:
                discarded_deck.append(player.cards.pop(0))
            if player.cards:
                discarded_deck.append(player.cards.pop(0))
        elif self.type == CardType.APOCALYPSE:
            if random.random() > 0.5:
                player.life -= 1
            else:
                player.life -= 2
        if self.value == CardValue.HEALING:
            player.life += 1
        if self.value == CardValue.EXTRA:
            player.points += 1
        if self.value == CardValue.EXTRA_:
            player.points += 2


