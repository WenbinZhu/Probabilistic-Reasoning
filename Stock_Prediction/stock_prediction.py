import os
import numpy as np

DATA_PATH = 'data/'
NASDAQ00 = os.path.join(DATA_PATH, 'nasdaq00.txt')
NASDAQ01 = os.path.join(DATA_PATH, 'nasdaq01.txt')

def stock_market_predict_from_2000():
    with open(NASDAQ00, 'r') as f00:
        lines = f00.readlines()
        prices = map(lambda s: float(s.strip()), lines)

        coefficients_x = []
        right_values = []

        for i in range(4):
            co_x = [np.array([prices[j+3], prices[j+2], prices[j+1], prices[j]]) * prices[j-i+3] for j in range(len(prices) - 4)]
            co_x = np.sum(co_x, axis=0)
            coefficients_x.append(co_x)

        for i in range(4):
            right_values.append(sum([prices[j-i+3] * prices[j+4] for j in range(len(prices) - 4)]))

        coefficients_x = np.asarray(coefficients_x)
        right_values = np.asarray(right_values)

        solution = np.linalg.solve(coefficients_x, right_values)
        print '(a)\nlinear coefficients (a1, a2, a3, a4) = ', tuple(solution.tolist())
        print '\n(b)'

        return solution


def stock_mean_squared_error(coefficients, year):
    assert year == 2000 or year == 2001
    price_file = NASDAQ00 if year == 2000 else NASDAQ01
    with open(price_file, 'r') as file:
        lines = file.readlines()
        prices = map(lambda s: float(s.strip()), lines)

        predictions = [np.sum(np.array(prices[i-4:i][::-1] * coefficients)) for i in range(4, len(prices))]

        print 'MSE for year %d = ' %(year,), np.mean(np.square(np.array(predictions) - np.array(prices[4:])))


if __name__ == '__main__':
    print '5.5 Stock market prediction\n'
    coefficients = stock_market_predict_from_2000()
    stock_mean_squared_error(coefficients, 2000)
    stock_mean_squared_error(coefficients, 2001)