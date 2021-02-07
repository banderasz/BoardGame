from CardValue import CardValue
from Card import Card
from Player import Player
from CardType import CardType

import random
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter, defaultdict
import pandas as pd
import seaborn as sns


class Game:
    def __init__(self, resources_num, players_num, card_pull, apocalypse_num, bonus_num, hand_limit, start_card, turns):
        self.resources_num = resources_num
        self.players_num = players_num
        self.card_pull = card_pull
        self.apocalypse_num = apocalypse_num
        self.bonus_num = bonus_num
        self.hand_limit = hand_limit
        self.start_card = start_card
        self.turns = turns
        self.statistics = defaultdict(lambda: defaultdict(lambda: 0))
        self.deck = []
        self.discarded_deck = []
        self.apocalypse_cards = []
        self.players = []
        self.current_turn = 0
        self.end = False

    def init_game(self):
        self.statistics = defaultdict(lambda: defaultdict(lambda: 0))
        self.deck = []
        for value in CardValue:
            if CardType.get_type(value) == CardType.RESOURCE:
                for i in range(self.resources_num):
                    self.deck.append(Card(value))
            elif CardType.get_type(value) == CardType.APOCALYPSE:
                for i in range(self.apocalypse_num):
                    self.deck.append(Card(value))
            elif CardType.get_type(value) == CardType.BONUS:
                for i in range(self.bonus_num):
                    self.deck.append(Card(value))
            elif CardType.get_type(value) == CardType.JUNK:
                for i in range(self.apocalypse_num*2):
                    self.deck.append(Card(value))
        random.shuffle(self.deck)
        self.discarded_deck = []
        self.players = []

        for i in range(self.players_num):
            self.players.append(Player(limit=self.hand_limit[self.players_num]))
            for _ in range(self.start_card):
                self.players[i].cards.append(Card(CardValue(random.randint(1, 8))))

    def player_died(self, player_):
        player_.died_turn = self.current_turn
        try:
            self.statistics["player_died"][max(self.statistics["player_died"].keys()) + 1] = self.current_turn
        except ValueError:
            self.statistics["player_died"][1] = self.current_turn


    def apocalypse(self, card):
        self.statistics["activated_in_turn"][self.current_turn] += 1
        new_players = []
        for player_ in self.players:
            if CardType.RESOURCE in player_.cards:
                self.discarded_deck.append(player_.cards.pop())
            else:
                card.effect(player_, self.discarded_deck)
            if CardType.RESOURCE in player_.cards:
                self.discarded_deck.append(player_.cards.pop())
            else:
                card.effect(player_, self.discarded_deck)
            if CardType.RESOURCE in player_.cards:
                self.discarded_deck.append(player_.cards.pop())
            else:
                card.effect(player_, self.discarded_deck)
            if player_.life > 0:
                new_players.append(player_)
            else:
                self.player_died(player_)


        self.players = new_players
        for player_ in self.players:
            player_.limit = self.hand_limit[len(self.players)]
        if len(self.players) <= 1:
            self.statistics["game_ended"]["game_ended"] = self.current_turn
            self.end = True

    def add_apocalypse_to_deck(self):
        for value in CardValue:
            if CardType.get_type(value) == CardType.APOCALYPSE:
                self.deck.append(Card(value))

    def pull(self, player):
        if len(self.deck) < len(self.players) * self.card_pull[len(self.players)]:
            self.deck.extend(self.discarded_deck)
            self.add_apocalypse_to_deck()
            random.shuffle(self.deck)
            self.discarded_deck = []
        card = self.deck.pop(0)
        if card.type == CardType.APOCALYPSE:
            self.statistics["apocalypse"][card.value] += 1
            self.discarded_deck.append(card)
            if self.statistics["apocalypse"][card.value] % 3 == 0:  # apocalypse is activated
                self.apocalypse(card)

        elif card.type == CardType.RESOURCE:
            player.cards.append(card)
            random.shuffle(player.cards)
            if len(player.cards) > player.limit:
                self.discarded_deck.append(player.cards.pop())
        elif card.type == CardType.BONUS:
            card.effect(player, self.discarded_deck)
            self.discarded_deck.append(card)

    def players_turn(self, player):
        player.points += 1
        for i in range(self.card_pull[len(self.players)]):
            self.pull(player)
            if self.end:
                break

    def turn(self):
        for player in self.players:
            self.players_turn(player)
            if self.end:
                break

    def game(self):
        while self.current_turn < self.turns:
            self.current_turn += 1
            self.turn()
            if self.end:
                self.statistics["players_alive"][self.current_turn] = len(self.players)
                break
            else:
                self.statistics["players_alive"][self.current_turn] = len(self.players)
                self.statistics["deck_num"][self.current_turn] = len(self.deck)
                self.statistics["discarded_deck_num"][self.current_turn] = len(self.discarded_deck)
                for player in self.players:
                    self.statistics["card_in_hand"][self.current_turn] += len(player.cards)
                self.statistics["card_in_hand_per_player"][self.current_turn] = self.statistics["card_in_hand"][
                                                                                    self.current_turn] / len(
                    self.players)
        self.statistics["game_ended"]["game_ended"] = self.current_turn


players_alive = list()
players_died = defaultdict(lambda: list())
apocalypse_activated = list()
deck_num = list()
discarded_deck_num = list()
cards_in_hand = list()
card_in_hand_per_player = list()
game_ended = list()

N = 1000

players_number = 3
for _ in range(N):
    game = Game(resources_num=10, players_num=players_number, card_pull={6: 3, 5: 4, 4: 5, 3: 8, 2: 10},
                apocalypse_num=8, bonus_num=8, hand_limit={6: 12, 5: 12, 4: 12, 3: 20, 2: 20, 1: 0, 0: 0}, turns=20, start_card=6)
    game.init_game()
    game.game()

    players_alive.append(pd.Series(game.statistics["players_alive"]))
    for i in range(players_number):
        players_died[i + 1].append(game.statistics["player_died"][i + 1])

    apocalypse_activated.append(pd.Series(game.statistics["activated_in_turn"]))
    deck_num.append(pd.Series(game.statistics["deck_num"]))
    discarded_deck_num.append(pd.Series(game.statistics["discarded_deck_num"]))
    cards_in_hand.append(pd.Series(game.statistics["card_in_hand"]))
    card_in_hand_per_player.append(pd.Series(game.statistics["card_in_hand_per_player"]))
    game_ended.append((game.statistics["game_ended"]["game_ended"]))

players_alive_df = pd.DataFrame(players_alive)
apocalypse_activated_df = pd.DataFrame(apocalypse_activated)
deck_num_df = pd.DataFrame(deck_num)
discarded_deck_num_df = pd.DataFrame(discarded_deck_num)
cards_in_hand = pd.DataFrame(cards_in_hand)
card_in_hand_per_player = pd.DataFrame(card_in_hand_per_player)

players_alive_df.mean().plot.bar()
plt.title("Players alive")
plt.show()
apocalypse_activated_df.mean().plot.bar()
plt.title("Apocalypse activated")
plt.show()

deck_num_df.boxplot()
plt.title("Deck size")
plt.show()
discarded_deck_num_df.boxplot()
plt.title("Discarded deck size")
plt.show()
cards_in_hand.boxplot()
plt.title("Cards in hand")
plt.show()
card_in_hand_per_player.boxplot()
plt.title("Cards in hand per player")
plt.show()

plt.hist(game_ended, bins=range(21))
plt.title("Game ended in turn")
plt.show()

for i in range(1, players_number):
    plt.hist(players_died[i], bins=range(21))
    plt.title("{}. death in turn in {} case".format(i, len(players_died[i])))
    plt.show()

# sns.violinplot(data=players_alive_df, inner="quartile", cut=0, split=True, linewidth=0)
# plt.show()
#
# sns.violinplot(data=players_alive_df, inner="box", cut=0, split=True, linewidth=0)
# plt.show()
#
# sns.violinplot(data=players_alive_df, inner="point", cut=0, split=True, linewidth=0)
# plt.show()
#
# sns.violinplot(data=players_alive_df, inner="stick", cut=0, split=True, linewidth=0)
# plt.show()
