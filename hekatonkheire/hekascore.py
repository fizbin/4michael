#!/usr/bin/env python3
#
# This is a python module - it is intended that other code will import
# this module, but that this code will not run on its own.

# cards are two character strings: the first character one of
# A23456789TJQK and the last one of HDCS, or the string "O1" or "O2"
# for the two jokers.

# all _check_* methods take a hand (iterable of cards) and return an
# iterable of (detailed kind name, score)

import collections
import itertools


def _noak_score(count):
    if count < 5:
        return 3 * (4 ** (count - 2))
    return 120 * (count - 4)


def _check_noak(hand):
    ranks = collections.Counter(x[0] for x in hand)
    n_jokers = ranks['O']
    del ranks['O']
    most_common = ranks.most_common()
    retval = []
    for (_, n) in most_common:
        en = n + n_jokers
        if en > 1:
            retval.append(('noak-%d' % (en,), _noak_score(en)))
    return retval


def _check_fullhouse(hand):
    ranks = collections.Counter(x[0] for x in hand)
    n_jokers = ranks['O']
    del ranks['O']
    most_common = ranks.most_common()
    if len(most_common) >= 2:
        (_, ncards1) = most_common[0]
        second_position = 1
        (_, ncards2) = most_common[second_position]
        while (n_jokers == 0 and ncards2 == ncards1
               and second_position < len(most_common) - 1):
            second_position += 1
            (_, ncards2) = most_common[second_position]
        retval = []
        for jokers_to_1 in range(n_jokers+1):
            ncards1_p = ncards1 + jokers_to_1
            ncards2_p = ncards2 + (n_jokers - jokers_to_1)
            if ncards1 > 1 and ncards2 > 1 and ncards1 != ncards2:
                noak_score1 = _noak_score(ncards1_p)
                noak_score2 = _noak_score(ncards2_p)
                retval.append(
                    ('fh-%d-%d' % (ncards1, ncards2),
                     min(200, noak_score1 * noak_score2)))
        return retval
    return []


def _check_fullhouse3(hand):
    # This is for FH that is three-noak FH
    ranks = collections.Counter(x[0] for x in hand)
    n_jokers = ranks['O']
    del ranks['O']
    most_common = ranks.most_common()
    if len(most_common) >= 3:
        (_, ncards1) = most_common[0]
        (_, ncards2) = most_common[1]
        third_position = 1
        (_, ncards3) = most_common[third_position]
        while (n_jokers == 0
               and ncards2 == ncards1
               and ncards3 == ncards2
               and third_position < len(most_common) - 1):
            third_position += 1
            (_, ncards3) = most_common[third_position]
        retval = []
        for joker_dist in itertools.combinations_with_replacement(
                [0, 1, 2], n_jokers):
            ncard_list = [ncards1, ncards2, ncards3]
            for spot in joker_dist:
                ncard_list[spot] += 1
            score = min(200,
                        _noak_score(ncard_list[0]) * _noak_score(ncard_list[1])
                        * _noak_score(ncard_list[2]))
            if not (ncard_list[0] == ncard_list[1]
                    and ncard_list[1] == ncard_list[2]):
                retval.append(('fh-%d-%d-%d' % tuple(ncard_list), score))
    return []


def _check_multipair(hand):
    ranks = collections.Counter(x[0] for x in hand)
    n_jokers = ranks['O']
    del ranks['O']
    most_common = ranks.most_common()
    n_pairs = len([nom for (nom, count) in most_common if count == 2])
    n_singletons = len([nom for (nom, count) in most_common if count == 1])
    joker_pairs = min(n_singletons, n_jokers)
    n_pairs += joker_pairs
    n_pairs += (n_jokers - joker_pairs) // 2
    if n_pairs > 1:
        return [('mp-%d' % (n_pairs,), 1 + 2 * n_pairs)]
    return []


def _check_multi3oak(hand):
    ranks = collections.Counter(x[0] for x in hand)
    n_jokers = ranks['O']
    del ranks['O']
    most_common = ranks.most_common()
    n_triples = len([nom for (nom, count) in most_common if count == 3])
    n_pairs = len([nom for (nom, count) in most_common if count == 2])
    n_singletons = len([nom for (nom, count) in most_common if count == 1])
    joker_triples_from_pairs = min(n_pairs, n_jokers)
    n_jokers -= joker_triples_from_pairs
    joker_triples_from_singletons = min(n_singletons, n_jokers // 2)
    n_jokers -= 2*joker_triples_from_singletons
    n_triples += joker_triples_from_pairs
    n_triples += joker_triples_from_singletons
    n_triples += n_jokers // 3
    if n_triples > 1:
        return [('m3oak-%d' % (n_triples,), 10 + 2 * n_triples)]
    return []


def _check_noak_flush(hand):
    cards = collections.Counter(hand)
    n_jokers = cards['O1'] + cards['O2']
    del cards['O1']
    del cards['O2']
    ((_, count),) = cards.most_common(1)
    count += n_jokers
    if count >= 2:
        return [('noakflush-%d' % (count,), [48, 64, 148, 340, 640][count - 2])]
    return []


def _check_flush(hand):
    suits = collections.Counter(x[1] for x in hand)
    n_jokers = suits['1'] + suits['2']
    del suits['1']
    del suits['2']
    ((_, n_cards),) = suits.most_common(1)
    if n_cards + n_jokers > 4:
        n_flush = n_cards + n_jokers
        return [('flush-%d' % (n_flush,), 10 + 15*(n_flush - 4))]
    return []


def _check_ncolor(hand):
    suits = collections.Counter(x[1] for x in hand)
    n_jokers = suits['1'] + suits['2']
    del suits['1']
    del suits['2']
    reds = n_jokers + suits['H'] + suits['D']
    blacks = n_jokers + suits['S'] + suits['C']
    if reds > blacks:
        if reds >= 6:
            return [('ncolor-%d' % (reds,), 5*reds - 10)]
    else:
        if blacks >= 6:
            return [('ncolor-%d' % (blacks,), 5*blacks - 10)]
    return []


def _check_john(hand):
    suits = collections.Counter(x[1] for x in hand)
    n_jokers = suits['1'] + suits['2']
    del suits['1']
    del suits['2']
    most_common = suits.most_common(2)
    if len(most_common) >= 2:
        (_, ncards1) = most_common[0]
        (_, ncards2) = most_common[1]
        if n_jokers == 0 and ncards1 == ncards2:
            second_index = 2
            while len(most_common) > second_index:
                (_, ncards2) = most_common[second_index]
                if ncards2 != ncards1:
                    break
                second_index += 1
            else:
                return []
        while n_jokers > 0:
            if ncards1 > ncards2 + 1:
                ncards2 += 1
            else:
                ncards1 += 1
            n_jokers -= 1
        if ncards2 >= 2:
            return [('john-%d-%d' % (ncards1, ncards2), 2*(ncards1 + ncards2))]
    return []


def _find_max_straight_len(hand, suit=None):
    n_jokers = len([x for x in hand if x[0] == 'O'])
    ranks = set(x[0] for x in hand
                if suit is None
                or x[1] == suit)

    all_ranks = 'A23456789TJQK'

    run_len = [0] * (n_jokers + 1)
    max_run_len = 0

    for rank in all_ranks * 2:
        if rank in ranks:
            for i in range(n_jokers + 1):
                run_len[i] += 1
        else:
            max_run_len = max(max_run_len, run_len[-1])
            for i in reversed(range(n_jokers)):
                run_len[i + 1] = run_len[i] + 1
            run_len[0] = 0

    max_run_len = min(max_run_len, len(all_ranks))
    return max_run_len


def _check_straight(hand):
    max_straight = _find_max_straight_len(hand)
    if max_straight > 6:
        return [('straight-%d' % max_straight, 70 + 30*(max_straight - 6))]
    if max_straight >= 4:
        return [('straight-%d' % max_straight, 6*(max_straight - 1))]
    return []


def _check_straight_flush(hand):
    max_straight = max(_find_max_straight_len(hand, suit)
                       for suit in 'HCDS')
    if max_straight > 6:
        return [(
            'straightflush-%d' % (max_straight,),
            (10 + 15*(max_straight - 4)) + (70 + 30*(max_straight - 6)))]
    if max_straight > 4:
        return [(
            'straightflush-%d' % (max_straight,),
            10 + 15*(max_straight - 4) + 6*(max_straight - 1))]
    return []


def _check_face_straight(hand):
    ranks = collections.Counter(x[0] for x in hand)
    n_jokers = ranks['O']
    del ranks['O']
    missing_faces = set('JQKA') - set(ranks)
    n_missing_faces = len(missing_faces)
    if n_missing_faces <= n_jokers:
        return [('facestraight-4', 37)]
    return []


def _check_bicycle(hand):
    ranks = collections.Counter(x[0] for x in hand)
    n_jokers = ranks['O']
    del ranks['O']
    all_ranks = 'A23456789TJQK'
    bicycle_length = 0
    for (idx, rank) in enumerate(all_ranks):
        if ranks[rank] == 0:
            if n_jokers == 0:
                bicycle_length = idx
                break
            else:
                n_jokers -= 1
    else:
        bicycle_length = len(all_ranks)
    if bicycle_length > 6:
        return [('bicycle-%d' % bicycle_length,
                 2*(70 + 30*(bicycle_length - 6)))]
    if bicycle_length >= 4:
        return [('bicycle-%d' % bicycle_length, 2*6*(bicycle_length - 1))]
    return []


def _check_royal_flush(hand):
    ranks = {}
    for x in hand:
        ranks.setdefault(x[0], set()).add(x[1])
    n_jokers = len(ranks.setdefault('O', set()))
    del ranks['O']
    royalf_ranks = 'JQKAT298'
    royal_length = 0
    for suit in 'HCDS':
        n_jokers_working = n_jokers
        for (idx, rank) in enumerate(royalf_ranks):
            if suit not in ranks.get(rank, set()):
                if n_jokers_working == 0:
                    royal_length = max(idx, royal_length)
                    break
                else:
                    n_jokers_working -= 1
        else:
            royal_length = max(len(royalf_ranks), royal_length)
    if royal_length >= 4:
        return [('royal-%d' % royal_length, 160+160*(royal_length - 3))]
    return []


def _check_evens(hand):
    ranks = set(x[0] for x in hand)
    n_jokers = len(list(x for x in hand if x[0] == 'O'))
    n_missing_evens = len(set('2468TQ') - ranks)
    if n_missing_evens <= n_jokers:
        return [('evens', 26)]
    return []


def _check_odds(hand):
    ranks = set(x[0] for x in hand)
    n_jokers = len(list(x for x in hand if x[0] == 'O'))
    n_missing_odds = len(set('A3579JK') - ranks)
    if n_missing_odds <= n_jokers:
        return [('odds', 37)]
    return []


def _rank_val(card):
    return 'OA23456789TJQK'.index(card[0])


def _check_sum_15(hand):
    n_jokers = len(list(x for x in hand if x[0] == 'O'))
    if n_jokers > 0:
        # If we have any jokers, there must be a way to make a
        # two-card sum to fifteen
        return [('sum-fifteen-2', 15)]
    hand_ranks = [_rank_val(x) for x in hand]
    # 89-90% of the time there's a two-card method, so check that first
    for (idx, rank_num) in enumerate(hand_ranks):
        if 15 - rank_num in hand_ranks[idx+1:]:
            return [('sum-fifteen-2', 15)]

    for card_count in range(2, min(3, len(hand))):
        # So the idea here is that we pull out card_count cards and then
        # see if the remaining cards contain the rank we need to get to
        # fifteen.
        for base_card_idxs in itertools.combinations(
                range(len(hand_ranks)-1), card_count):
            chosen_sum = 0
            for idx in base_card_idxs:
                chosen_sum += hand_ranks[idx]
            if 15 - chosen_sum in hand_ranks[base_card_idxs[-1]+1:]:
                return [('sum-fifteen-%d' % (card_count + 1),
                         30 // (card_count + 1))]
    return []


def _check_low_high(hand):
    ranks = set(x[0] for x in hand)
    n_jokers = len(list(x for x in hand if x[0] == 'O'))
    if n_jokers > 0:
        return [('high-low', 0*14)]
    n_sevens = len(list(x for x in hand if x[0] == '7'))
    if n_sevens > 1:
        return [('high-low', 0*14)]
    for test in ('AK', '2Q', '3J', '4T', '59', '68'):
        if set(test) < ranks:
            return [('high-low', 0*14)]
    return []


CHECKS = (
    _check_noak,
    _check_john,
    _check_flush,
    _check_ncolor,
    _check_multipair,
    _check_bicycle,
    _check_straight,
    _check_fullhouse,
    _check_fullhouse3,
    _check_royal_flush,
    _check_face_straight,
    _check_straight_flush,
    _check_evens,
    _check_odds,
    _check_sum_15,
    _check_low_high,
    _check_multi3oak,
    _check_noak_flush,
    )


def check_hand(hand):
    retval = []
    for checker in CHECKS:
        r = checker(hand)
        if r:
            r = [max(r, key=lambda x: x[1])]
        retval.extend(r)
    retval.sort(key=lambda x: x[1], reverse=True)
    return retval
