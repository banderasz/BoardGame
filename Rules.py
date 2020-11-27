class Rules:

    def __init__(self, deck, players):
        self.deck = deck
        self.players = players

    def check_resource(self, card, player):
        pass

    def effect(self, card, player):
        if card.value == 9:
            if self.check_resource(card, player) == 3:
                player.cards = []
            elif self.check_resource(card, player) == 2:
                for player_ in self.players:
                    if player != player_:
                        player_.cards.append(player.cards.pop())
            elif self.check_resource(card, player) == 1:
                player.cards.pop()
