import java.util.ArrayList;

/**
 * Created by Wenbin Zhu.
 */
public class GameTest {

    public static void main(String[] argv) {
        GameGuess gameGuess = new GameGuess();

        ArrayList<GuessResult> guessResults = new ArrayList<>();

        guessResults.add(gameGuess.getBestGuess("-----", ""));
        guessResults.add(gameGuess.getBestGuess("-----", "AI"));
        guessResults.add(gameGuess.getBestGuess("A---R", ""));
        guessResults.add(gameGuess.getBestGuess("A---R", "E"));
        guessResults.add(gameGuess.getBestGuess("--U--", "ODLC"));
        guessResults.add(gameGuess.getBestGuess("-----", "EO"));
        guessResults.add(gameGuess.getBestGuess("D--I-", ""));
        guessResults.add(gameGuess.getBestGuess("D--I-", "A"));
        guessResults.add(gameGuess.getBestGuess("-U---", "AEIOS"));


        for (GuessResult guessResult : guessResults) {
            System.out.print("best next guess l: ");
            System.out.println(guessResult.getBestGuess());
            System.out.print("P(Li = l | E): ");
            System.out.println(guessResult.getBestProbability());
            System.out.println();
        }
    }
}
