using System;
using System.Collections.Generic;


namespace SeekRF8
{
    class MainClass
    {
        // Draw a random hand; is it a royalflush-8?
        public static bool IsRandomHandRF8(Random random)
        {
            // Assume that we laid the cards out all sorted
            // so that they were AH AH 2H 2H ... KH KH AS AS ...
            // and then the four jokers at the end
            // Now number each card from 0 to 107 (there are 108 cards)
            // Jokers are then the last four cards (cards 104, 105, 106, 107)
            // for non-jokers, suit is determined by (card number) / 26
            // (round down), and rank is ((card % 26) / 2) + 1, where the
            // division is rounded down, and the "+1" is to make a 2 have
            // rank 2, etc.
            List<int> chosen = new List<int>(10);
            for(int i=0; i < 8; i++)
            {
                int card = random.Next(108);
                while(chosen.Contains(card))
                {
                    card = random.Next(108);
                }
                chosen.Add(card);
            }
            // now check for the same suit
            // suit will be card / 26, one of 0-3
            int? suit = null;
            for (int i = 0; i < 8; i++)
            {
                if (chosen[i] >= 104) continue; // Jokers
                if (suit.HasValue)
                {
                    if ((chosen[i] / 26) != suit)
                        return false;
                }
                else
                {
                    suit = chosen[i] / 26;
                }
            }
            // if we reached here, we have all the same suit, plus jokers
            // now check for [8,9,T,J,Q,K,A,2]
            // be careful to reject if we have two non-jokers with the same rank
            List<int> required_ranks = new List<int>
            {
                8, 9, 10, 11, 12, 13, 1, 2
            };
            for (int i = 0; i < 8; i++)
            {
                if (chosen[i] >= 104) continue;
                int rank = (((chosen[i] % 26) / 2) + 1);
                if (required_ranks.Contains(rank))
                {
                    required_ranks.Remove(rank);
                }
                else
                {
                    return false;
                }
            }
            // okay, got through everything
            return true;
        }
        public static void Main(string[] args)
        {
            int handcount = 0;
            long iteration = 0;
            Random rnd = new Random();
            for (int j = 1; j <= 100; j++)
            {
                for (long i = 1; i <= 10000000; i++)
                {
                    handcount += IsRandomHandRF8(rnd) ? 1 : 0;
                    iteration += 1;
                }
                Console.WriteLine("Iteration: {0} royal-flush-8: {1}",
                    iteration, handcount);
            }
        }
    }
}
