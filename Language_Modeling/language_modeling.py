import os
import numpy as np
import matplotlib.pyplot as plt

np.seterr(divide='ignore')

DATA_PATH = 'data/'
VOCAB_PATH = os.path.join(DATA_PATH, 'vocab.txt')
UNIGRAM_PATH = os.path.join(DATA_PATH, 'unigram.txt')
BIGRAM_PATH = os.path.join(DATA_PATH, 'bigram.txt')

class LM(object):
    def __init__(self):
        vocab = np.loadtxt(VOCAB_PATH, dtype='str')
        bigram = np.loadtxt(BIGRAM_PATH, dtype='int32')
        bigram_0, bigram_1, bigram_2 = bigram[:, 0], bigram[:, 1], bigram[:, 2]

        # use defaultdict to get 0 when key is not in dict
        # prevent key checks for unobserved words
        self.vocab = dict(zip(vocab, [i + 1 for i in range(vocab.shape[0])]))
        self.vocab_list = vocab
        self.unigram = np.loadtxt(UNIGRAM_PATH, dtype='int32')
        self.bigram = dict(zip(zip(bigram_0, bigram_1), bigram_2))

        self.unigram_counts = np.sum(self.unigram)


    def get_unigram_prob(self, token):
        return self.unigram[self.vocab[token] - 1] / float(self.unigram_counts)


    def get_bigram_prob(self, token1, token2, verborse=False):
        if not (self.vocab[token1], self.vocab[token2]) in self.bigram:
            bi_cnt = 0
            if verborse:
                print 'unobserved words: {0} {1}'.format(token1, token2)
        else:
            bi_cnt = self.bigram[(self.vocab[token1], self.vocab[token2])]

        return bi_cnt / float(self.unigram[self.vocab[token1] - 1])


    def make_sentence_unigram_list(self, sentence):
        sentence_unigram_list = map(lambda t: t.upper(), sentence.split(' '))
        for i in range(len(sentence_unigram_list)):
            if not sentence_unigram_list[i] in self.vocab:
                sentence[i] = '<UNK>'

        return sentence_unigram_list

    def make_sentence_bigram_list(self, sentence):
        sentence_unigram_list = self.make_sentence_unigram_list(sentence)

        sentence_bigram_list = [('<s>', sentence_unigram_list[0])]
        for i in range(len(sentence_unigram_list) - 1):
            sentence_bigram_list.append((sentence_unigram_list[i], sentence_unigram_list[i + 1]))

        return sentence_bigram_list

    def unigram_distribution(self, startswith):
        target_tokens = filter(lambda s: s.startswith(startswith), self.vocab.keys())
        for i, token in enumerate(sorted(target_tokens)):
            print '{:<5}\t{:<20}\t{:<20}'.format(i, token, self.get_unigram_prob(token))


    def bigram_distribution(self, word):
        bigram_counts =sum(tup[1] for tup in self.bigram.items())
        target_tokens = filter(lambda s: s[0][0] == self.vocab[word.upper()], self.bigram.items())

        for i, token in enumerate(sorted(target_tokens, key=lambda tk : -tk[1])[0 : 5]):
            print '{:<5}\t{:<20}\t{:<20}'.format(i, self.vocab_list[token[0][1] - 1], float(token[1]) / bigram_counts)

    def uni_bi_compare(self, sentence):
        sentence_unigram_list = self.make_sentence_unigram_list(sentence)
        sentence_bigram_list = self.make_sentence_bigram_list(sentence)

        L_u = sum(np.log([self.get_unigram_prob(token) for token in sentence_unigram_list]))
        L_b = sum(np.log([self.get_bigram_prob(token1, token2, True) for token1, token2 in sentence_bigram_list]))

        print 'L_u = {0}\nL_b = {1}'.format(L_u, L_b)


    def mixture_model(self, sentence):
        lambda_list = np.linspace(0, 1, 1000)[:]
        sentence_bigram_list = self.make_sentence_bigram_list(sentence)
        lm_history = []

        for l in lambda_list:
            L_m = sum(np.log([(1 - l) * self.get_unigram_prob(token2) + l * self.get_bigram_prob(token1, token2) \
                          for token1, token2 in sentence_bigram_list]))
            lm_history.append(L_m)

        max_index = np.argmax(lm_history)
        print 'Max L_m = {}\nOptimal lambda = {:.3}'.format(lm_history[max_index], lambda_list[max_index])

        plt.plot(lambda_list, lm_history, '-g')
        plt.xlabel("lambda")
        plt.ylabel("L_m probability")
        # plt.show()


if __name__ == '__main__':
    lm = LM()

    print '-'*8 + ' 4.3 Statistical language modeling ' + '-' * 8
    print '-' * 50
    print '(a) Unigram probabilities start with A:'
    lm.unigram_distribution('A')
    print '-'*50

    print '\n' + '-' * 50
    print '(b) Five most likely words following "THE":'
    lm.bigram_distribution('The')
    print '-' * 50

    print '\n' + '-' * 50
    print '(c) Log-likelihoods of the sentence under the unigram and bigram models:'
    lm.uni_bi_compare("Last week the stock market fell by one hundred points")
    print '-' * 50

    print '\n' + '-' * 50
    print '(d) Log-likelihoods of another sentence under the unigram and bigram models:'
    lm.uni_bi_compare("The nineteen officials sold fire insurance")
    print '\nThe effect of unobserved words on the log-likelihood from the bigram model is that' \
          + 'the probability of these words is zero and the log calculation of the probability becomes -infinite'
    print '-' * 50

    print '\n' + '-' * 50
    print '(e) Mixture model: optimal lambda:'
    lm.mixture_model("The nineteen officials sold fire insurance")
    print '-' * 50
