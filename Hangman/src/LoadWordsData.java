import java.io.*;
import java.util.*;


/**
 * Created by Wenbin Zhu.
 */

// Class for load data and compute most/least frequent words
public class LoadWordsData {

    private int totalCount = 0;
    private HashMap<String, Integer> wordsCount = new HashMap<>();
    private final String dataPath = "data/hw1_word_counts_05.txt";
    public final int wordLength = Integer.parseInt(dataPath.split("\\/|\\.")[1].split("_")[3]);

    LoadWordsData() {
        try (BufferedReader br = new BufferedReader(new FileReader(dataPath))) {
            String line = br.readLine();
            while (line != null) {
                String word = line.split(" ")[0];
                Integer count = Integer.valueOf(line.split(" ")[1]);
                wordsCount.put(word, count);

                totalCount += count;
                line = br.readLine();
            }
        } catch (FileNotFoundException fnfEx) {
            fnfEx.printStackTrace();
        } catch (IOException ioEx) {
            ioEx.printStackTrace();
        }

    }


    public int getTotalCount() {
        return this.totalCount;
    }


    public HashMap<String, Integer> getWordsCount() {
        return this.wordsCount;
    }


    public ArrayList<ArrayList<String>> getMostLeastFrequent(int mostNum, int leastNum) {
        int wordsSize = wordsCount.size();
        assert mostNum > 0 && mostNum < wordsSize;
        assert leastNum > 0 && leastNum < wordsSize;

        ArrayList<String> mostFrequentList = new ArrayList<>(mostNum);
        ArrayList<String> leastFrequentList = new ArrayList<>(leastNum);
        ArrayList<ArrayList<String>> result = new ArrayList<>(2);

        List<Map.Entry<String, Integer>> orderedWords = new ArrayList<>(wordsCount.entrySet());

        Collections.sort(orderedWords, new Comparator<Map.Entry<String, Integer>>() {

            @Override
            public int compare(Map.Entry<String, Integer> o1, Map.Entry<String, Integer> o2) {
                return o2.getValue().compareTo(o1.getValue());
            }
        });

        for (int i = 0; i < mostNum; i++)
            mostFrequentList.add(orderedWords.get(i).getKey());

        for (int i = wordsSize - 1; i >= wordsSize - leastNum; i--)
            leastFrequentList.add(orderedWords.get(i).getKey());

        result.add(mostFrequentList);
        result.add(leastFrequentList);

        return result;
    }

}
