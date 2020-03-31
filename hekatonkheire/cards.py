#!/usr/bin/env python3

import random

ALL_SUITS = 'HCDS'
ALL_RANKS = 'A23456789TJQK'
FULL_DECK = ['O1', 'O2'] + [
    rank + suit
    for rank in ALL_RANKS
    for suit in ALL_SUITS]


def random_hand(size=8, allow_jokers=True, rnd=random):
    double_deck = FULL_DECK + FULL_DECK
    if not allow_jokers:
        double_deck.remove('O1')
        double_deck.remove('O1')
        double_deck.remove('O2')
        double_deck.remove('O2')

    return rnd.sample(double_deck, size)
