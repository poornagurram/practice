# the cross entropy is the sum of the label elements times the natural log of the prediction probabilities
# Cross-entropy is a measure of the difference between two probability distributions for a
# given random variable or set of events.

import numpy as np

label_vector = np.array([0, 0, 0, 1, 0]) # one hot encoding
predcn_prob = np.array([0.27, 0.11, 0.33, 0.10, 0.19])


def cross_entropy(labels,probs):
    return -np.dot(labels, np.log(probs))


if __name__ == '__main__':
    print(cross_entropy(label_vector, predcn_prob))
