# coding=utf-8
'''
    TEMPLATE FOR MACHINE LEARNING HOMEWORK
    AUTHOR Eric Eaton
'''

import numpy as np
from collections import Counter
from numpy.lib.scimath import log
from numpy.ma import exp


# def get_probs_per_feature(feature, num_instances):
#     return {feature_val: count / num_instances
#             for feature_val, count in Counter(feature)}
#
#
# def get_probs(features, laplaceSmoothing=True):
#     """
#     :param features: matrix with features as columns and values as rows
#     :return: dictionary {feature value: probability}
#     """
#     num_instances, num_features = features.shape
#     return features.sum(axis=0)
#
#     return {get_probs_per_feature(feature, num_instances)
#             for feature in features.T}
#
#
# def create_conditional_probs_dict(X, y):
#     conditional_probs_dict = {}
#     for klass in np.unique(y):
#         x_klass = X[y == klass]
#         conditional_probs_dict[klass] = get_probs(x_klass)


class NaiveBayes:
    def __init__(self, useLaplaceSmoothing=True):
        """
        Constructor
        """
        self.useLaplaceSmoothing = useLaplaceSmoothing


    def fit(self, X, y):
        """
        Trains the model
        Arguments:
            X is a n-by-d numpy array
            y is an n-dimensional numpy array
        """
        # self.classes = np.unique(y)
        # self.conditional_probs_dict = create_conditional_probs_dict(X, y)
        # y = np.matrix(y).T
        # self.y_probs = get_probs(y)


    def predict(self, X):
        """
        Used the model to predict values for each instance in X
        Arguments:
            X is a n-by-d numpy array
        Returns:
            an n-dimensional numpy array of the predictions
        """
        # conditiona_probs_matrix = create_conditional_probs_matrix(
        #     self.classes, self.conditional_probs_dict, X)
        # return get_argmax_y(conditiona_probs_matrix, self.classes)


    def predictProbs(self, X):
        """
        Used the model to predict a vector of class probabilities for each instance in X
        Arguments:
            X is a n-by-d numpy array
        Returns:
            an n-by-K numpy array of the predicted class probabilities (for K classes)
        """
        # return scores_to_probs(scores)


# def prob_instance_given_y(prob_y, list_prob_features_given_y):
#     return prob_y + sum(list_prob_features_given_y)
#
#
# def get_list_prob_features_given_y(conditional_probs_dict, X, feature, klass):
#     return [conditional_probs_dict[x][feature, klass]
#             for x in X[feature, :]]
#
#
# def create_conditional_probs_matrix(classes, conditional_probs_dict, X):
#     return np.fromfunction(
#         lambda i, j: prob_instance_given_y(classes[j], [
#             get_list_prob_features_given_y(
#                 conditional_probs_dict, X, i, j  # i=feature, j=class
#             )
#         ])
#     )


def get_argmax_y(conditional_probs_matrix, classes):
    return classes(conditional_probs_matrix.argmax(axis=1))


class OnlineNaiveBayes:
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
        if self.useLaplaceSmoothing:
            laplaceSmoothingVals = get_laplace_smoothing_vals()
        else:
            laplaceSmoothingVals = None
        self.lg_theta = get_lg_theta_per_class(self.feature_counts, laplaceSmoothingVals)
        self.class_priors = get_class_priors(self.class_counts)

    def predict(self, X):
        """
        Used the model to predict values for each instance in X
        Arguments:
            X is a n-by-d numpy array
        Returns:
            an n-dimensional numpy array of the predictions
        """
        scores = get_scores_given_class(X, self.classes, self.class_priors, self.lg_theta)
        best_scores = scores.argmax(axis=1)
        return self.classes[best_scores]


    def predictProbs(self, X):
        """
        Used the model to predict a vector of class probabilities for each instance in X
        Arguments:
            X is a n-by-d numpy array
        Returns:
            an n-by-K numpy array of the predicted class probabilities (for K classes)
        """
        scores = get_scores_given_class(X, self.classes, self.class_priors, self.lg_theta)
        return scores_to_probs(scores)

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
        feature_counts += 1
        total_count += laplaceSmoothingVals
    return log(np.true_divide(feature_counts, total_count))


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
    prob_instances = exp(scores.sum(axis=1))
    scores = (exp(scores)).T
    return np.divide(scores, prob_instances)
