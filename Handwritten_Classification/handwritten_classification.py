import os
import numpy as np
import matplotlib.pyplot as plt

DATA_PATH = 'data/'
TRAIN_3 = os.path.join(DATA_PATH, 'train3.txt')
TRAIN_5 = os.path.join(DATA_PATH, 'train5.txt')
TEST_3 = os.path.join(DATA_PATH, 'test3.txt')
TEST_5 = os.path.join(DATA_PATH, 'test5.txt')

# np.random.seed(seed=12345)

class HandWritten(object):
    def __init__(self):
        with open(TRAIN_3, 'r') as ftrain_3:
            lines = self.readlines_format(ftrain_3)
            self.train_3_num = len(lines)
            self.train_x = np.array(lines, dtype='int')
            self.train_y = np.array([1] * self.train_3_num)

        with open(TRAIN_5, 'r') as ftrain_5:
            lines = self.readlines_format(ftrain_5)
            self.train_5_num = len(lines)
            self.train_x = np.concatenate([self.train_x, np.array(lines, dtype='int')], axis=0)
            self.train_y = np.concatenate([self.train_y, np.array([0] * self.train_5_num)])

        # shuffle train data
        # self.train_x, self.train_y = self.shuffle(self.train_x, self.train_y)
        self.train_num = self.train_x.shape[0]

        # self.w = np.random.standard_normal([64])
        self.w = np.zeros([64])


    # Newton method
    def train_newton(self):
        i = 0
        error_rates = []
        log_likelihoods = []

        print 'Training...'
        while not self.check_convergence(log_likelihoods, 0.001, 5):
            dot = np.dot(self.train_x, self.w.reshape([64, 1]))
            sig = self.sigmoid(dot)
            diff = self.train_y.reshape([self.train_num, -1]) - sig
            derivative = np.dot(self.train_x.T, diff)
            hessian = np.zeros([64, 64])

            for t in range(self.train_num):
                product = np.sum(self.w * self.train_x[t].flatten())
                hessian -= self.sigmoid(product) * self.sigmoid(-product) * \
                           np.dot(self.train_x[t].reshape([64, 1]), self.train_x[t].reshape([1, 64]))
                # hessian -= self.sigmoid(product) * self.sigmoid(-product) * np.outer(self.train_x[t], self.train_x[t])

            self.w -= np.dot(np.linalg.inv(hessian), derivative).flatten()
            y_pred = self.sigmoid(np.dot(self.train_x, self.w.reshape([64, 1]))).flatten()

            error_rates.append(self.get_error_rate(y_pred, self.train_y))
            log_likelihoods.append(self.get_log_likelihood(self.train_y, self.w, self.train_x))

            i += 1
            print 'epoch {0}, log likelihood = {1}, error rate = {2}%'.format(i, log_likelihoods[i - 1], error_rates[i - 1])

        self.print_weights()
        self.plot_error_likelihood(range(i), error_rates, log_likelihoods)


    # gradient ascend method
    def train_gradient_ascend(self, lr):
        i = 0
        error_rates = []
        log_likelihoods = []

        while not self.check_convergence(log_likelihoods, 0.001, 5):
            sig = self.sigmoid(np.dot(self.train_x, self.w.reshape([64,1])))
            diff = self.train_y.reshape([self.train_num, -1]) - sig
            derivative = np.dot(self.train_x.T, diff)

            self.w += lr / self.train_num * derivative.flatten()
            y_pred = self.sigmoid(np.dot(self.train_x, self.w.reshape([64,1]))).flatten()

            error_rates.append(self.get_error_rate(y_pred, self.train_y))
            log_likelihoods.append(self.get_log_likelihood(self.train_y, self.w, self.train_x))

            i += 1
            print 'epoch {0}, log likelihood = {1}, error rate = {2}%'.format(i, log_likelihoods[i - 1], error_rates[i - 1])

        self.print_weights()
        self.plot_error_likelihood(range(i), error_rates, log_likelihoods)


    def testing(self):
        with open(TEST_3, 'r') as ftest_3:
            lines = self.readlines_format(ftest_3)
            self.test_3_num = len(lines)
            self.test_x = np.array(lines, dtype='int')
            self.test_y = np.array([1] * self.test_3_num)

        with open(TEST_5, 'r') as ftest_5:
            lines = self.readlines_format(ftest_5)
            self.test_5_num = len(lines)
            self.test_x = np.concatenate([self.test_x, np.array(lines, dtype='int')], axis=0)
            self.test_y = np.concatenate([self.test_y, np.array([0] * self.test_5_num)])

        self.text_num = self.test_x.shape[0]

        y_pred = self.sigmoid(np.dot(self.test_x, self.w.reshape([64, 1]))).flatten()

        error_rate = self.get_error_rate(y_pred, self.test_y)
        log_likelihood = self.get_log_likelihood(self.test_y, self.w, self.test_x)

        print 'Test result:\nlog likelihood = {0}, error rate = {1}%'.format(log_likelihood, error_rate)


    def get_log_likelihood(self, y, w, x):
        log_likelihood = 0
        for t in range(y.shape[0]):
            dot = np.sum(w * x[t].flatten())
            log_likelihood += y[t] * np.log(self.sigmoid(dot)) + (1 - y[t]) * np.log(self.sigmoid(-dot))

        return log_likelihood


    def get_error_rate(self, y_pred, y):
        y_pred = np.array(y_pred >= 0.5, dtype='int')

        return sum(y_pred != y) / float(y.shape[0]) * 100

    def shuffle(self, train_x, train_y):
        concat = np.concatenate([train_x, train_y.reshape([-1,1])], axis=1)
        np.random.shuffle(concat)
        return concat[:, 0:64], concat[:, 64]

    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-x))


    def readlines_format(self, file_handler):
        lines = file_handler.readlines()
        return map(lambda s: s.strip().split(), lines)

    def check_convergence(self, log_likelihoods, confidence, limit):
        if len(log_likelihoods) < limit:
            return False

        diff = np.abs(np.array(log_likelihoods[-limit+1:]) - np.array(log_likelihoods[-limit:-1]))
        return sum(diff < confidence) == limit - 1

    def print_weights(self):
        print '\nWeight Matrix(8*8):\n'
        for i in self.w.reshape([8,8]):
            for j in i:
                print '{:5f}'.format(j),
            print ''

    def plot_error_likelihood(self, t, error_rates, log_likelihoods):
        plt.title('Error Rates and Log likelihoods')

        plt.subplot(2, 1, 1)
        plt.plot(t, log_likelihoods, color='green')
        plt.xlabel('epoch')
        plt.ylabel('log likelihood')

        plt.subplot(2, 1, 2)
        plt.plot(t, error_rates, color='red')
        plt.xlabel('epoch')
        plt.ylabel('error rate')


if __name__ == '__main__':
    print '5.6 Handwritten digit classification'
    print 'Using Newton\'s method\n'
    hw = HandWritten()
    print '(a)'
    # hw.train_gradient_ascend(0.08)
    hw.train_newton()
    print '\n(b)'
    hw.testing()
    plt.show()