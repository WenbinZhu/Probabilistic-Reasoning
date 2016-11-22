import os
import numpy as np

DATA_PATH = os.path.join(os.path.curdir, 'data')
PA1 = os.path.join(DATA_PATH, 'prob_a1.txt')
PA2 = os.path.join(DATA_PATH, 'prob_a2.txt')
PA3 = os.path.join(DATA_PATH, 'prob_a3.txt')
PA4 = os.path.join(DATA_PATH, 'prob_a4.txt')
RWS = os.path.join(DATA_PATH, 'rewards.txt')

rows = 81
gamma = 0.9925
total_actions = 4
pa1 = np.zeros([rows, rows])
pa2 = np.zeros([rows, rows])
pa3 = np.zeros([rows, rows])
pa4 = np.zeros([rows, rows])
rewards = np.zeros([rows])

vk = np.zeros([rows])
valid_states = [3, 11, 12, 15, 16, 17, 20, 22, 23, 24, 26, 29, 30, 31, 34, 35,\
                39, 43, 48, 52, 53, 56, 57, 58, 59, 60, 61, 62, 66, 70, 71]
direction_map = {0: 'west', 1: 'north', 2: 'east', 3: 'south'}

def read_files():
    read_pa_file(pa1, PA1)
    read_pa_file(pa2, PA2)
    read_pa_file(pa3, PA3)
    read_pa_file(pa4, PA4)
    read_rw_file(rewards, RWS)

def read_pa_file(pai, file):
    with open(file, 'r') as fp:
        for line in map(lambda l: l.strip(), fp.readlines()):
            s, s_, p = int(line.split()[0]) - 1, int(line.split()[1]) - 1, float(line.split()[2])
            pai[s][s_] = p

def read_rw_file(rw, file):
    with open(file, 'r') as fp:
        for i, r in enumerate(map(lambda l: l.strip(), fp.readlines())):
            rewards[i] = r


def value_iteration():
    for i in xrange(2000):
        for s in xrange(rows):
            estimations = [sum(pa[s][s_] * vk[s_] for s_ in xrange(rows)) for pa in [pa1, pa2, pa3, pa4]]
            vk[s] = rewards[s] + gamma * max(estimations)

    print 'non-zero values of V*(s):'
    for s, v in enumerate(vk):
        if v != 0.0:
            print '%d: %f' %(s+1, v)

def get_optimal_policy_from_value_iteraton():
    directions = {}

    for s in xrange(rows):
        estimations = [sum(pa[s, s_] * vk[s_] for s_ in xrange(rows)) for pa in [pa1, pa2, pa3, pa4]]
        if s + 1 in valid_states:
            directions[s + 1] = direction_map[np.argmax(estimations)]

    print '\noptimal policy:'
    print directions


def get_optimal_policy_from_policy_iteraton(initial=None):
    if initial == None:
        policy = np.random.randint(4, size=rows, dtype='int')
    else:
        assert initial >=0 and initial <= 3
        policy = np.ones([rows], dtype='int') * initial

    mdp_matrix = np.zeros([rows, rows])
    v_old, v = np.zeros([rows]), np.ones([rows])
    iteration = 0

    while not check_convergence(v_old, v, atol=0.01):
        iteration += 1
        v_old = v

        # policy evaluation
        for i in xrange(rows):
            pa = globals()['pa' + str(policy[i]+1)]
            mdp_matrix[i] = [-gamma * pa[i][j] for j in xrange(rows)]
            mdp_matrix[i][i] += 1
        v = np.dot(np.linalg.inv(mdp_matrix), rewards.reshape([-1, 1]))

        # policy improvement
        for s in xrange(rows):
            estimations = [sum(pa[s, s_] * v[s_] for s_ in xrange(rows)) for pa in [pa1, pa2, pa3, pa4]]
            policy[s] = np.argmax(estimations)

    print '\niteration times: ', iteration - 1

def check_convergence(vk_old, vk_new, atol):
    vk_old, vk_new = vk_old.flatten(), vk_new.flatten()
    for s in xrange(rows):
        if not np.isclose(vk_old[s], vk_new[s], atol=atol):
            return False

    return True


if __name__ == '__main__':
    read_files()

    value_iteration()
    get_optimal_policy_from_value_iteraton()
    get_optimal_policy_from_policy_iteraton(2)
    get_optimal_policy_from_policy_iteraton(3)
