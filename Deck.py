from CardType import CardType
from CardValue import CardValue


class Deck(list):

    def __contains__(self, item):
        if isinstance(item, CardType):
            for card in self:
                if card.type == item:
                    return card
            else:
                return None
        elif isinstance(item, CardValue):
            for card in self:
                if card.value == item:
                    return card
            else:
                return None
