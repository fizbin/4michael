using System;

namespace HandCount
{
    class MainClass
    {
        const int deckSize = 52;
        const int totalHandSize = 8;
        ulong[,] knownAnswers = new ulong[totalHandSize + 1, deckSize + 1];

        ulong getNumHands(int handSize, int deckSize)
        {
            if (handSize == 0)
            {
                return 1;
            }
            if (handSize < 0)
            {
                return 0;
            }
            if (deckSize <= 0)
            {  // note that handSize == 0, deckSize == 0 was covered above.
                return 0;
            }
            if (knownAnswers[handSize, deckSize] != 0)
            {
                return knownAnswers[handSize, deckSize];
            }
            knownAnswers[handSize, deckSize] = getNumHands(handSize, deckSize - 1)
                                             + getNumHands(handSize - 1, deckSize - 1)
                                             + getNumHands(handSize - 2, deckSize - 1);
            return knownAnswers[handSize, deckSize];
        }

        ulong getTotalHands()
        {
            return getNumHands(totalHandSize - 4, deckSize)
                 + getNumHands(totalHandSize - 3, deckSize)
                 + getNumHands(totalHandSize - 2, deckSize)
                 + getNumHands(totalHandSize - 1, deckSize)
                 + getNumHands(totalHandSize, deckSize);
        }
        public static void Main(string[] args)
        {
            Console.WriteLine(new MainClass().getTotalHands());
        }
    }
}
