import java.util.ArrayList;

/**
 * Created by Wenbin Zhu.
 */
public class SanityCheck {

    private static void printMostLeastFrequent(ArrayList<ArrayList<String>> mostLeastFrequent, int choice) {
        String title = choice == 0 ? "Most Frequent:" : "Least Frequent:";
        System.out.println(title);

        for (int i = 0; i < mostLeastFrequent.get(choice).size(); i++) {
            System.out.print(i + 1);
            System.out.println("\t" + mostLeastFrequent.get(choice).get(i));
        }
        System.out.println();
    }

    public static void main(String[] argv) {
        LoadWordsData wordsData = new LoadWordsData();

        ArrayList<ArrayList<String>> mostLeastFrequent = wordsData.getMostLeastFrequent(15, 14);

        printMostLeastFrequent(mostLeastFrequent, 0);
        printMostLeastFrequent(mostLeastFrequent, 1);
    }


}
