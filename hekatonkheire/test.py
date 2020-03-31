import cards
import hekascore
import random

if __name__ == '__main__':
    d = {}
    h = {}
    s = {}
    t = {}
    samp = {}
    beats = {}
    rnd = random.Random(834220936)
    for _ in range(5 * 1000 * 1000):
        hand = cards.random_hand(rnd=rnd)
        scores = hekascore.check_hand(hand)
        (winner, winscore) = scores[0]
        d[winner] = d.get(winner, 0) + 1
        t[winscore] = t.get(winscore, 0) + 1
        samp[winner] = repr(hand)
        for (thing, score) in scores:
            s[thing] = score
        for thing in set(x[0] for x in scores):
            h[thing] = h.get(thing, 0) + 1
            beats.setdefault(thing, {})[winner] = beats.setdefault(
                thing, {}).get(winner, 0) + 1
            samp.setdefault(thing, samp[winner] + '\t' + winner)
    with open("/tmp/a.tsv", "w") as f:
        for x in sorted(h):
            print("%s\t%d\t%d\t%d" % (x, h[x], d.get(x, 0), s[x]), file=f)
    melds = sorted(h)
    with open("/tmp/b.tsv", "w") as f:
        print('\t'.join([''] + melds), file=f)
        for x in melds:
            print('\t'.join([x] + [str(beats[x].get(y, ''))
                                   for y in melds]), file=f)
    with open("/tmp/samp.tsv", "w") as f:
        for x in melds:
            print('%s\t%s' % (x, samp.get(x, '')), file=f)
