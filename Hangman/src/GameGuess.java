import java.util.HashMap;
import java.util.Map;

/**
 * Created by Wenbin Zhu.
 */

class GuessResult {
    private char bestGuess;
    private double bestProbability;

    GuessResult(char bestGuess, double bestProbability) {
        this.bestGuess = bestGuess;
        this.bestProbability = bestProbability;
    }

    public char getBestGuess() {
        return bestGuess;
    }

    public double getBestProbability() {
        return bestProbability;
    }
}


// Class for show best next guess & its probability
public class GameGuess {

    private LoadWordsData wordsData = new LoadWordsData();

    // get best next guess and its probability
    public  GuessResult getBestGuess(String correctGuess, String wrongGuess) {
        double maxProbability = 0.0;
        char bestGuess = 'A';

        for (char guess = 'A'; guess <= 'Z'; guess = (char)(guess + 1)) {
            double oneGuessProbability = getOneGuessProbability(correctGuess, wrongGuess, guess);
            if (oneGuessProbability > maxProbability) {
                maxProbability = oneGuessProbability;
                bestGuess = guess;
            }
        }

        return new GuessResult(bestGuess, maxProbability);
    }

    // get Probability for any one guess
    public double getOneGuessProbability(String correctGuess, String wrongGuess, char guess) {
        assert correctGuess.length() == wordsData.wordLength;

        guess = Character.toUpperCase(guess);
        correctGuess = correctGuess.toUpperCase();
        wrongGuess = wrongGuess.toUpperCase();

        if (wrongGuess.indexOf(guess) != -1 || correctGuess.indexOf(guess) != -1)
            return 0.0;

        double resultProbability = 0.0;
        HashMap<String, Integer> wordsCount = wordsData.getWordsCount();

        // sum over all possible w
        for (Map.Entry<String, Integer> entry : wordsCount.entrySet()) {
            String word = entry.getKey();
            int count = entry.getValue();

            double pLgivenW = 0.0, pWgivenE = 0.0;
            double pNumerator = 0.0, pDenominator = 0.0;

            // compute p(Li = l for some i in {1,2,3,4,5} | W = w)
            for (int i = 0; i < word.length(); i++) {
                if (correctGuess.charAt(i) == '-' && word.charAt(i) == guess) {
                    pLgivenW = 1.0;
                    break;
                }
            }

            // compute p(W = w | E) using Beyes Rule
            for (Map.Entry<String, Integer> innerEntry : wordsCount.entrySet()) {
                String innerWord = innerEntry.getKey();
                int innerCount = innerEntry.getValue();

                double pEgivenW = 1.0;  // P(E | W = w)
                double pW = (double)innerCount / (double)wordsData.getTotalCount(); // P(W = w)

                for (int i = 0; i < innerWord.length(); i++) {
                    if ((correctGuess.charAt(i) != '-' && correctGuess.charAt(i) == innerWord.charAt(i))
                        || (correctGuess.charAt(i) == '-' && wrongGuess.indexOf(innerWord.charAt(i)) == -1
                                                         && correctGuess.indexOf(innerWord.charAt(i)) == -1)) {
                        continue;
                    }
                    pEgivenW = 0.0;
                    break;
                }

                if (innerWord.equals(word))
                    pNumerator = pW * pEgivenW;
                pDenominator += pW * pEgivenW;
            }

            pWgivenE = pNumerator / pDenominator;
            resultProbability += pLgivenW * pWgivenE;
        }

        return resultProbability;
    }

}
