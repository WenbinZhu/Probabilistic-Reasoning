import java.io.BufferedReader;
import java.io.FileReader;

/**
 * Created by robin Zhu
 */

public class EmNoisyOR {
    private int T = 0;
    private int N;
    private double[] Pi;
    private int[][] X;
    private int[] Y;
    private double[][] Infer;

    EmNoisyOR(String xPath, String yPath) {
        try {
            BufferedReader brX = new BufferedReader(new FileReader(xPath));
            BufferedReader brY = new BufferedReader(new FileReader(yPath));
            BufferedReader brT = new BufferedReader(new FileReader(yPath));


            // get the number of examples
            while (brT.readLine() != null)
                T++;

            X = new int[T][];
            Y = new int[T];

            String line;
            for (int i = 0; (line = brX.readLine()) != null; i++) {
                String[] sp = line.split(" ");
                X[i] = new int[sp.length];
                for (int s = 0; s < sp.length; s++)
                    X[i][s] = Integer.parseInt(sp[s]);
            }

            for (int i = 0; (line = brY.readLine()) != null; i++) {
                Y[i] = Integer.parseInt(line);
            }

            N = X[0].length;
            Infer = new double[T][N];
            Pi = new double[N];
            for (int j = 0; j < Pi.length; j++)
                Pi[j] = 1.0 / N;

        } catch (Exception e) {
            e.getStackTrace();
        }
    }

    public void eStep() {
        double[] pYgivenX = getPyGivenX();

        for (int t = 0; t < T; t++) {
            for (int j = 0; j < N; j++) {
                Infer[t][j] = Y[t] == 0 || X[t][j] == 0 ? 0 : Pi[j] / pYgivenX[t];
            }
        }
    }

    public void mStep() {
        for (int j = 0; j < N; j++) {
            int Ti = 0;
            Pi[j] = 0;
            for (int t = 0; t < T; t++) {
                Pi[j] += Infer[t][j];
                Ti += X[t][j] == 1 ? 1 : 0;
            }
            Pi[j] /= Ti;
        }
    }

    public void emEstimate(int iteration) {
        System.out.println(0 + " " + getNumOfMistakes() + " " + String.format("%.5f", getLogLikelihood()));
        int cond = 0;
        for (int i = 0; i < iteration; i++) {
            eStep();
            mStep();

            if (Math.abs((Math.log((double)i + 1) / Math.log(2)) - cond) < 0.0001) {
                System.out.println(i + 1 + " " + getNumOfMistakes() + " " + String.format("%.5f", getLogLikelihood()));
                cond++;
            }
        }
    }

    public int getNumOfMistakes() {
        int num = 0;
        double[] pYgivenX = getPyGivenX();

        for (int t = 0; t < T; t++) {
            int yPred = pYgivenX[t] >= 0.5 ? 1 : 0;
            num += yPred != Y[t] ? 1 : 0;
        }

        return num;
    }

    public double getLogLikelihood() {
        double[] pYgivenX = getPyGivenX();
        double logLikelihood = 0;

        for (int t = 0; t < T; t++) {
            logLikelihood += Y[t] == 1 ? Math.log(pYgivenX[t]) : Math.log(1 - pYgivenX[t]);
        }

        return logLikelihood / T;
    }

    public double[] getPyGivenX() {
        double product;
        double[] pYgivenX = new double[T];

        for (int t = 0; t < T; t++) {
            product = 1;
            for (int j = 0; j < N; j++) {
                product *= X[t][j] == 1 ? 1 - Pi[j] : 1;
            }

            pYgivenX[t] = 1 - product;
        }

        return pYgivenX;
    }

    public static void main(String[] args) {
        String dataPath = "data/";
        String xPath = dataPath + "spectX.txt";
        String yPath = dataPath + "spectY.txt";

        EmNoisyOR em = new EmNoisyOR(xPath, yPath);
        em.emEstimate(256);
    }
}
