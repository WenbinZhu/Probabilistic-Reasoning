import os
import numpy as np
import matplotlib.pyplot as plt

DATA_PATH = 'data/'
INIT_STATE_PATH = os.path.join(DATA_PATH, 'initialStateDistribution.txt')
TRANSITION_PATH = os.path.join(DATA_PATH, 'transitionMatrix.txt')
EMISSION_PATH = os.path.join(DATA_PATH, 'emissionMatrix.txt')
OBSERVATION_PATH = os.path.join(DATA_PATH, 'observations.txt')

class Viterbi(object):
    def __init__(self):
        with open(INIT_STATE_PATH) as f1, open(TRANSITION_PATH) as f2, \
             open(EMISSION_PATH) as f3, open(OBSERVATION_PATH) as f4:

            self.inital_states = np.array(map(lambda s: s.strip(), f1.readlines()), dtype='float32')
            self.transition = np.array(self.readlines_format(f2), dtype='float32')
            self.emission = np.array(self.readlines_format(f3), dtype='float32')
            self.observation = np.array(self.readlines_format(f4), dtype='int').flatten()

            self.n = self.inital_states.shape[0]
            self.T = self.observation.shape[0]

    def get_viberbi_path(self):
        self.l_matrix = self.get_l_matrix()
        sentence = ""

        viterbi_path = np.zeros([self.T], dtype='int')
        viterbi_path[self.T-1] = np.argmax(self.l_matrix[:, self.T - 1])

        for i in xrange(self.T-2, -1, -1):
            viterbi_path[i] = np.argmax(self.l_matrix[:, i] + np.log(self.transition[:, viterbi_path[i+1]]))

        viterbi_path += 1

        sentence += (chr(ord('a') + viterbi_path[0] - 1))
        for i in xrange(1, len(viterbi_path)):
            if viterbi_path[i] != viterbi_path[i - 1]:
                sentence += (chr(ord('a') + viterbi_path[i] - 1))

        return viterbi_path, sentence

    def get_l_matrix(self):
        l_matrix = np.zeros([self.n, self.T])
        l_matrix[:, 0] = np.log(self.inital_states) + np.log(self.emission[:, self.observation[0]])

        for i in xrange(1, self.T):
            lit_aij = np.tile(l_matrix[:, i-1], (self.n, 1)) + np.log(self.transition.T)
            l_matrix[:, i] = np.max(lit_aij, axis=1) + np.log(self.emission[:, self.observation[i]])

        return l_matrix

    def readlines_format(self, file):
        lines = file.readlines()
        return map(lambda s: s.strip().split(), lines)

    def plot_states(self, states):
        t = xrange(1, len(states) + 1)
        plt.plot(t, states, '-g')
        plt.xlabel('Time t')
        plt.ylim(0, 26)
        plt.ylabel('Most Likely State')
        plt.show()


if __name__ == '__main__':
    v = Viterbi()
    states, sentence = v.get_viberbi_path()

    print 'Most Likely States: ', states.tolist()
    print 'Decodeded sentence: ', sentence

    v.plot_states(states)

