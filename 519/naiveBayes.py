# coding=utf-8
'''
    TEMPLATE FOR MACHINE LEARNING HOMEWORK
    AUTHOR Eric Eaton
'''

import numpy as np
from collections import Counter
from numpy.lib.scimath import log
from numpy.ma import exp


class masterNaiveBayes:
    def __init__(self, useLaplaceSmoothing=True):
        """
        Constructor
        """
        self.useLaplaceSmoothing = useLaplaceSmoothing
        self.classes = np.array([])
        self.class_counts = {}
        self.feature_counts = {}
        self.unique_feature_vals = []

    def fit(self, X, y):
        """
        515
        Trains the model
        Arguments:
            X is a n-by-d numpy array
            y is an n-dimensional numpy array
        """
        self.classes = get_new_classes(y, self.classes)
        update_class_counts(y, self.class_counts)
        update_feature_counts(X, y, self.feature_counts)
        update_unique_feature_vals(X, self.unique_feature_vals)

    def get_scores(self, X):
        if self.useLaplaceSmoothing:
            laplaceSmoothingVals = get_laplace_smoothing_vals(self.unique_feature_vals)
        else:
            laplaceSmoothingVals = None
        self.lg_theta = get_lg_theta(
            self.class_counts, self.feature_counts, laplaceSmoothingVals
        )
        self.class_priors = get_class_priors(self.class_counts)
        return get_scores_given_class(X, self.classes, self.class_priors, self.lg_theta)

    def predict(self, X):
        """
        Used the model to predict values for each instance in X
        Arguments:
            X is a n-by-d numpy array
        Returns:
            an n-dimensional numpy array of the predictions
        """
        best_scores = (self.get_scores(X)).argmax(axis=1)
        return self.classes[best_scores]


    def predictProbs(self, X):
        """
        Used the model to predict a vector of class probabilities for each instance in X
        Arguments:
            X is a n-by-d numpy array
        Returns:
            an n-by-K numpy array of the predicted class probabilities (for K classes)
        """
        return scores_to_probs(self.get_scores(X))


class NaiveBayes(masterNaiveBayes):
    pass

class OnlineNaiveBayes(masterNaiveBayes):
    pass


def get_new_classes(y, classes):
    return np.unique(np.append(y, classes))


def update_class_counts(y, counts):
    """
    :param y: y is an n-dimensional numpy array
    :param counts: dict {class: counts of class}
    """
    counter = Counter(y)
    for klass in counter:
        if klass not in counts:
            counts[klass] = 0
        counts[klass] += counter[klass]


def update_feature_counts(X, y, counts):
    """
    :param X: X is a n-by-d numpy array
    :param y: y is an n-dimensional numpy array
    :param counts: dict {class: array[[counts per feature]]}
    """
    for klass in np.unique(y):
        if klass not in counts:
            counts[klass] = 0
        counts[klass] += X[y == klass].sum(axis=0)


def update_unique_feature_vals(X, unique_vals):
    """
    :param X: X is a n-by-d numpy array
    :param unique_vals: list of sets of unique values for each feature
    """
    if not unique_vals:
        for _ in X[0, :]:
            unique_vals.append(set())
            # assumes alll inputs have same number of features
    for row in X:
        for j in range(row.size):
            unique_vals[j].add(row[j])


def get_lg_theta_per_class(feature_counts, laplaceSmoothingVals):
    """
    :param feature_counts: array[[counts per feature]]
    :param laplaceSmoothingVals: either None or
        array[[size(unique values) for each feature]]
    :return: array[[ log(P(feature | class) ]] for each feature
    """
    total_count = feature_counts.sum()
    if laplaceSmoothingVals is not None:
        feature_counts_ = feature_counts + 1
        total_count_ = total_count + laplaceSmoothingVals
    return log(np.true_divide(feature_counts_, total_count_))


def get_laplace_smoothing_vals(unique_feature_vals):
    return np.array([len(vals) for vals in unique_feature_vals])


def get_lg_theta(class_counts, feature_counts, laplaceSmoothingVals):
    """
    :param class_counts: dict {class: num occurrences}
    :param feature_counts: dict {class: array[[counts per feature]]}
    :param laplaceSmoothingVals: either None or
        array[[size(unique values) for each feature]]
    :return dict {class: array[[ log(theta_cj) ]]}
    """
    return {
        klass: get_lg_theta_per_class(feature_counts[klass], laplaceSmoothingVals)
        for klass in class_counts
    }


def get_class_priors(class_counts):
    """
    :param class_counts: dict {class: num_instances}
    :return: dict {class: log(P(class))}
    """
    num_instances = float(sum(class_counts.values()))
    return {klass: log(class_counts[klass] / num_instances)
            for klass in class_counts}


def get_scores_given_class(X, classes, class_probs, lg_theta):
    """

    :param classes:
    :param X: training instances
    :param class_probs: dict {class: log(P(class))}
    :param lg_theta: dict {class: array[[ log(theta_cj) ]]}
    :return: |instances|x|classes| matrix, vals ∝ log(P(class))
    """

    def get_prob(instance, klass_index):
        instance = int(instance)
        klass = classes[int(klass_index)]
        return class_probs[klass] + np.dot(X[instance, :], lg_theta[klass])

    return np.fromfunction(np.vectorize(get_prob), (len(X), len(class_probs)))


def scores_to_probs(scores):
    """
    :param scores: |instances|x|classes| matrix, vals ∝ log(P(class))
    :return:  |instances|x|classes| matrix, vals = log(P(class))
    """
    prob_instances = exp(scores.sum(axis=1))
    scores = (exp(scores)).T
    return np.divide(scores, prob_instances)
