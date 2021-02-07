from enum import Enum
from CardValue import CardValue

class CardType(Enum):
    RESOURCE = 1
    APOCALYPSE = 2
    BONUS = 3
    JUNK = 4

    @classmethod
    def get_type(cls, card_value: CardValue):
        if 1 <= card_value.value <= 8:
            return CardType.RESOURCE
        elif 9 <= card_value.value <= 14:
            return CardType.APOCALYPSE
        elif 15 <= card_value.value <= 20:
            return CardType.BONUS
        elif 21 <= card_value.value <= 21:
            return CardType.JUNK
