import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.Random;


/**
 * Created by Wenbin Zhu.
 */
public class LWsimulation {

    private int[] Bi;
    private double alpha;
    private int zValue;
    private int[] bIndices;
    private int significantBits;
    private Random rand = new Random(System.currentTimeMillis());

    LWsimulation(int nBits, double alpha, int zValue, int[] bIndices, int significantBits) {
        assert bIndices.length <= nBits;

        this.alpha = alpha;
        this.zValue = zValue;
        this.bIndices = bIndices;
        this.significantBits = significantBits;
        this.Bi = new int[nBits];
    }


    public ArrayList<ArrayList<Double>> getProbabilities() {
        ArrayList<ArrayList<Double>> resultProbs = new ArrayList<>();

        for (int idx = 0; idx < bIndices.length; idx++) {
            System.out.println("Estimating B" + bIndices[idx] + ":");
            double pNumerator = 0.0, pDenominator = 0.0;

            int numSamples = 0, checkPoint = 1000;
            ArrayList<Double> biProb = new ArrayList<>();

            while (true) {
                int funcB = 0;
                double pZgivenB;

                for (int i = 0; i < Bi.length; i++) {
                    // Bi[i] = Math.random() < 0.5 ? 0 : 1;
                    Bi[i] = rand.nextInt(2);
                    funcB += Math.pow(2, i) * Bi[i];
                }

                pZgivenB = (1 - alpha) / (1 + alpha) * Math.pow(alpha, Math.abs(zValue - funcB));

                if (Bi[bIndices[idx] - 1] == 1)
                    pNumerator += pZgivenB;
                pDenominator += pZgivenB;

                if (++numSamples == checkPoint) {
                    biProb.add(pNumerator / pDenominator);
                    System.out.println(numSamples + " samples: " + (pNumerator / pDenominator));

                    if (checkPoint < 1000000)
                        checkPoint *= 10;
                    else
                        checkPoint += 1000000;

                    if (biProb.size() >= 3 && checkConvergence(biProb, significantBits))
                        break;
                }
            }

            resultProbs.add(biProb);
            System.out.println();
        }

        return resultProbs;
    }


    private boolean checkConvergence(ArrayList<Double> biProb, int significantBits) {
        int size = biProb.size();
        String[] b1 = getScientificNotation(biProb.get(size - 1), significantBits);
        String[] b2 = getScientificNotation(biProb.get(size - 2), significantBits);
        String[] b3 = getScientificNotation(biProb.get(size - 3), significantBits);

        return b1[0].equals(b2[0]) && b2[0].equals(b3[0]) &&
                b1[1].equals(b2[1]) && b2[1].equals(b3[1]);
    }

    private String[] getScientificNotation(double probability, int significantBits) {
        String[] s = String.format("%." + significantBits + "E", probability).split("E");
        s[0] = s[0].substring(0, s[0].length() - 1);

        return s;
    }


    public static void main(String[] args) {
        int[] Bi = new int[]{2, 4, 6, 8, 10};
        LWsimulation lW= new LWsimulation(10, 0.2, 128, Bi, 3);
        ArrayList<ArrayList<Double>> resultProbs = lW.getProbabilities();

        try {
            PrintWriter writer = new PrintWriter("estimation_history.txt", "UTF-8");
            for (int i = 0; i < resultProbs.size(); i++) {
                writer.print("B" + Bi[i] + " ");
                for (Double prob : resultProbs.get(i)) {
                    writer.print(prob + " ");
                }
                writer.println();
            }

            writer.close();
        } catch (FileNotFoundException fnfE) {
            fnfE.printStackTrace();
        } catch (UnsupportedEncodingException ueE) {
            ueE.printStackTrace();
        }

    }

}
